#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Flask Restful Website
# ========================================================================

#import modules, I use the sys library to use files in different folders
import sys
sys.path.append('./file_uploader_ingest')
from file_uploader_ingest import *
sys.path.append('./NLP_analysis')
from NLP_analysis import *
sys.path.append('./newsfeed_ingest')
from newsfeed_ingest import *
import db
from db import updateDB
from db import encodeJSON

#flask, flask_restful
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './File_Data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

#MongoDB JSON encoder
import json
from bson import ObjectId

#other libraries
from datetime import datetime
import os
from urllib.parse import unquote #url parsing in readlater rest api component

#################################

app = Flask(__name__)

for key in keys_collection.find():
	if (key.get('name') == "Flask"):
		app.secret_key = key.get('key')

app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app) 

parser = reqparse.RequestParser()
parser.add_argument('UserInfo', location='form')
parser.add_argument('FileInfo', location='form')
app_users = []
app_files = []				 		 

app_users, app_files = updateDB()
	
@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')

@app.route('/signup', methods=['GET'])
def signup():
	return render_template('signup.html')

@app.route('/success', methods=['GET'])
def success():
	return render_template('success.html')	

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')

@app.route('/homepage', methods=['GET'])
def homepage():
	session['readlater_lock'] = False #Make sure readlater list loads each time
	return render_template('homepage.html')	

@app.route('/upload', methods=['GET'])
def upload():
	return render_template('upload.html')			

@app.route('/fileview', methods=['GET'])
def fileview():
	return render_template('fileview.html')

@app.route('/analyzer', methods=['GET'])
def analyzer():
	return render_template('analyzer.html')	

@app.route('/newsfeed', methods=['GET'])
def newsfeed():
	return render_template('newsfeed.html')

@app.route('/search', methods=['GET'])
def search():
	DiscoverContent()

@app.route('/editfile', methods=['GET'])
def editfile():
	return render_template('editfile.html')

@app.route('/readlater', methods=['GET'])
def readlater():
	return render_template('readlater.html')

@app.route('/numfiles', methods=['GET'])
def numfiles():
	return render_template('numfiles.html')			
# @app.route('/test_db')
# def test_db():
# 	test_user = {
# 		'U_ID': -1, 
# 		'Username': "mongodb", 
# 		'FirstName': "Data", 
# 		'LastName': "Base"
# 	}
# 	db.users_db.user_collection.insert_one(test_user)	
# 	return "Uploaded test user to MongoDB!"	

class User(Resource):
	#http://127.0.0.1:5000/users/0
	def get(self, uid):
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			for user in app_users:
				if user.get('U_ID') == uid:
					return user
			return "U_ID does not exist"

	#http://127.0.0.1:5000/users/login
	def post(self, uid):
		method = uid
		error = None
		if (method == "login"):
			uname = request.form.get("login_username")
			pword = request.form.get("login_password")
			# print("uname and pword:")
			# print(request)
			# print(uname)
			# print(pword)
			for user in app_users:
				if ((user.get('Username') == uname) and (user.get('Password') == pword)):
					session['username'] = uname
					session['firstname'] = user.get('FirstName')
					session['lastname'] = user.get('LastName')
					session['uid'] = user.get('U_ID')
					session['load_lock'] = False
					session['readlater_lock'] = True
					session['num_files'] = 1 #default uploading 1 file on upload screen
					return redirect(url_for("homepage"))
			# print("Failure")
			flash("Credentials do not match.")
			return redirect(url_for("login"))	
		else:
			return redirect(url_for("login"))			

	#curl http://127.0.0.1:5000/users/2 -X DELETE -v
	def delete(self, uid):
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			global app_users
			global app_files
			for user in app_users:
				if user.get('U_ID') == uid:
					query = {"U_ID": uid}
					db.users_db.user_collection.delete_one(query)
					app_users, app_files = updateDB() 
					return f"Deleted user with U_ID: {uid}"
			return "U_ID does not exist"

	#curl http://127.0.0.1:5000/users/0 -d "UserInfo=ljstaib12345, Luke, Staib" -X PUT -v
	def put(self, uid): #edit info
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			global app_users
			global app_files
			args = parser.parse_args()
			for user in app_users:
				if user.get('U_ID') == uid:
					query = {"U_ID": uid}
					userinfo = list(args['UserInfo'].split(", "))
					if (len(userinfo) != 4):
						return "To edit an existing user, UserInfo is a list of THREE arguments."
					uname = userinfo[0]
					pword = userinfo[1]
					fname = userinfo[2]
					lname = userinfo[3]
					readlater = userinfo[4]
					updated_user = { "$set": {
						'Username': uname,
						'Password': pword, 
						'FirstName': fname, 
						'LastName': lname,
						'ReadLaterList': readlater,
					}}
					db.users_db.user_collection.update_one(query, updated_user)
					app_users, app_files = updateDB()
					return updated_user
			return "U_ID does not exist"


class UserList(Resource):
	#http://127.0.0.1:5000/users
	def get(self):
		return app_users

	#curl http://127.0.0.1:5000/users -d "UserInfo=ljs123, Luke, Staib" -X POST -v
	#CURL is outdated, use website to post now
	#Right now, in order: username, first name, last name
	#then check GET method
	def post(self):
		global app_users
		global app_files
		max_uid = 0
		for user in app_users:
			if user.get('U_ID') > max_uid:
				max_uid = user.get('U_ID')
		new_uid = max_uid + 1
		# print('Request: ')
		# print(request)

		new_uname = request.form.get("create_username")
		new_pword = request.form.get("create_password")
		new_fname = request.form.get("create_firstname")
		new_lname = request.form.get("create_lastname")

		# args = parser.parse_args()
		# print("args:")
		# print(args)
		# new_userinfo = list(args['UserInfo'].split(", "))
		# if (len(new_userinfo) != 3):
		# 	return "To create a new user, UserInfo is a list of THREE arguments."
		# # print(new_userinfo)
		# new_uname = new_userinfo[0]
		# new_fname = new_userinfo[1]
		# new_lname = new_userinfo[2]
		new_user = {
			'U_ID': new_uid, 
			'Username': new_uname, 
			'Password': new_pword,
			'FirstName': new_fname, 
			'LastName': new_lname,
			'ReadLaterList': [],
		}	
		db.users_db.user_collection.insert_one(new_user)
		app_users, app_files = updateDB()
		# new_user = (encodeJSON().encode(new_user)).replace(r'\"', '"')
		# new_user = json.JSONDecoder().decode(new_user)
		# app_users.append(new_user)
		return redirect(url_for("success"))

class File(Resource):
	#http://127.0.0.1:5000/files/0
	def get(self, fid, method):
		global app_users
		global app_files
		try:
			fid = int(fid)
		except ValueError:
			return "Invalid F_ID, must be an int"
		else:	
			for file in app_files:
				if file.get('F_ID') == fid:
					if (method == "analyze"):
						text_data = file.get('Text')
						keywords = CreateKeywords(text_data)
						sentiment = AssessData(text_data)
						try:
							categories = ObtainCategories(text_data)
						except:
							categories = {}

						updated_file = { "$set": {
							'Sentiment': sentiment, 
							'Tags': {
								'Status': "Analyzed",
								'Keywords': keywords,
								'Categories': categories,
							}
						}}
						query = {"F_ID": fid}
						#print(query)
						#print(updated_file)
						files_collection.update_one(query, updated_file)
						app_users, app_files = updateDB()
						flash('File with name ' + str(file.get('Name')) + ' successfully analyzed.')
						session['load_lock'] = False
						return redirect(url_for("homepage"))
					if (method == "edit"):
						edit_data = [] #set edit data as a list
						edit_data.append(fid) #index 0
						edit_data.append(str(file.get('Name'))) #index 1
						edit_data.append(str(file.get('Authors'))) #index 2
						edit_data.append(str(file.get('CreationTime'))) #index 3
						session['edit_data'] = edit_data
						return redirect(url_for("editfile"))
					if (method == "delete"):
						if (FileDelete(fid) == True):
							app_users, app_files = updateDB()
							flash('File with name ' + str(file.get('Name')) + ' successfully deleted.')
							session['load_lock'] = False
							return redirect(url_for("homepage"))
						else:
							flash('There was a problem deleting ' + str(file.get('Name')) + '. Please try again later.')
							return redirect(url_for("homepage"))		
					else:	
						return file	
			return f'File with ID {fid} does not exist'

	def post(self, fid, method):
		#edit info
		try:
		    fid = int(fid)
		except ValueError:
		    return "Please enter a valid F_ID (int)"
		else: 
			global app_users
			global app_files
			if (method == "edit"):
				for file in app_files:
					if file.get('F_ID') == fid:
						authors = request.form.get("edit_authors")
						filename = session['edit_data'][1]
						creation_time = str(request.form.get("edit_month") + "/" + request.form.get("edit_day") + "/" + request.form.get("edit_year"))
						if (FileEdit(fid, authors, creation_time) == True):
							app_users, app_files = updateDB()
							flash(f'File {filename} successfully edited.')
							session['load_lock'] = False
							return redirect(url_for('homepage'))
						else:
							flash(f'File {filename} could not be edited. Please try again later.')
							return redirect(url_for('homepage'))
			else:
				return "Invalid method"		
			return "F_ID does not exist"										

class FileList(Resource):
	#http://127.0.0.1:5000/files
	def get(self):
		return app_files

	#curl http://127.0.0.1:5000/files -d "FileInfo=FileName1, TXT, John Doe, 01/02/1980 00:00:00, 0, 100, Uploaded" -X POST -v
	#then check GET method
	def post(self):
		global app_users
		global app_files
		#args = parser.parse_args()
		# print(args)
		max_fid = -1
		for file in app_files:
			if file.get('F_ID') > max_fid:
				max_fid = file.get('F_ID')

		files_uploaded = session['num_files']
		for i in range(files_uploaded):		
			fid = max_fid + 1
			max_fid = fid

			file_var = 'file' + str(i + 1)

			if (file_var) not in request.files:
				print("ERROR: No files found when uploading.")
				flash('No file part')
				return redirect("/homepage")
			file = request.files[file_var]
			if file.filename == '':
				print("ERROR: No files selected.")
				flash('No selected file')
				return redirect("/homepage")

			authors = request.form.get("authors")
			creation_time = str(request.form.get("month") + "/" + request.form.get("day") + "/" + request.form.get("year"))
			if session['uid'] != None:	
				new_file = UploadFiles(session['uid'], file, fid, authors, creation_time)
				print("File created") 
			else:
				new_file = UploadFiles(-1, file, fid, authors, creation_time) #-1 is not authenticated
		#Command line method:
		# new_fileinfo = list(args['FileInfo'].split(", "))
		# if (len(new_fileinfo) != 7):
		# 	return "To create a new file, FileInfo is a list of SEVEN arguments."
		# #print(new_fileinfo)
		# filename = new_fileinfo[0]
		# filetype = new_fileinfo[1]
		# authors = new_fileinfo[2]
		# text = ""
		# creation_time = new_fileinfo[3]
		# source = new_fileinfo[4]
		# filesize = new_fileinfo[5]
		# status = new_fileinfo[6]
		# upload_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

			if (new_file == False):
				flash(f'There was a problem uploading your file. Please try again later.')
				success = False
			else:
				session['load_lock'] = False
				files_collection.insert_one(new_file)
				app_users, app_files = updateDB()
				flash(f'File uploaded successfully.')
				success = True

		if (success == True):
			return redirect(url_for("homepage"))
		else:
			return redirect(url_for("upload"))					

class UserFiles(Resource):
	#http://127.0.0.1:5000/ufiles/0/homepage
	def get(self, uid, page): #page refers to the webpage to redirect to
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			files_data = [] #For all files, list of lists
			for user in app_users:
				if user.get('U_ID') == uid:
					for file in app_files:
						if file.get('Source') == uid:
							file_data = [] #For each file
							file_data.append(file.get('F_ID')) #fid, 0
							#file_data.append(file) #file
							file_data.append(file.get('Name')) #filename, 1
							file_data.append(file.get('Authors')) #authors, 2
							upload_time = str(file.get('UploadTime'))
							upload_time = upload_time.split(" ")
							upload_time = upload_time[0]
							file_data.append(upload_time) #upload time, 3
							file_data.append(file.get('CreationTime')) #date of article, 4
							file_data.append(file.get('Tags').get('Status')) #status, 5
							if (file.get('Tags').get('Keywords')):
								file_data.append(", ".join(file.get('Tags').get('Keywords')[:5])) #1st 5 keywords, 6
							else:	
								file_data.append("N/A")
							if (file.get('Tags').get('Categories') != {}):
								file_data.append(file.get('Tags').get('Categories')) #1st 5 categories, 7
							else:	
								file_data.append("N/A")	
							if file.get('Sentiment') != None: #score and magnitude of sentiment, 8
								score_val = file.get('Sentiment').get('score')
								score_val = float(score_val[:-1])
								score_val = score_val / 10
								if (score_val < -0.2):
									score = "Negative"
								elif (score_val > 0.2):
									score = "Positive"	
								else:
									score = "Neutral"

								magnitude_val = file.get('Sentiment').get('magnitude')
								magnitude_val = float(magnitude_val[:-1])
								magnitude_val = magnitude_val / 10
								if (magnitude_val < 0.5):
									magnitude = "Weakly expressed"
								elif (magnitude_val > 0.5 and magnitude_val < 1.5):
									magnitude = "Expressed neither strongly nor weakly"
								else:
									magnitude = "Strongly expressed"

								file_data.append("Sentiment: " + score + "       |       Magnitude of Sentiment: " + magnitude)
							else:
								file_data.append("N/A")

							files_data.append(file_data)	

			session['load_lock'] = True
			session['files_data'] = files_data
			if (len(files_data) > 0):
				return redirect(url_for(page))
			else:	
				session['files_data'] = None
				return redirect(url_for(page))	

class Searcher(Resource):	
	#http://127.0.0.1:5000/search/election/0
	def get(self, query): #page refers to search results page (0-99)	
		results = DiscoverContent(query)
		if (results == False):
			flash("There was a problem searching. Please try again later.")	
			return redirect(url_for('newsfeed'))
		else:
			flash(results)
			return redirect(url_for('newsfeed'))	

class SaveReadLater(Resource):
	#http://127.0.0.1:5000/savelink/0/'https://website.com/article.html'
	def get(self, uid, url): #page refers to the webpage to redirect to
		global app_users
		global app_files
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			for user in app_users:
				if user.get('U_ID') == uid:
					query = {"U_ID": uid}
					url = unquote(url)
					updated_user = { "$push": {
						'ReadLaterList': url,
					}}
					db.users_db.user_collection.update_one(query, updated_user)
					app_users, app_files = updateDB()
					session['readlater_lock'] = False
					flash("Saved article link to your read later list!")
					return redirect(url_for('homepage'))

class LoadReadLater(Resource):
	#http://127.0.0.1:5000/loadlinks/0
	def get(self, uid): #page refers to the webpage to redirect to
		global app_users
		global app_files
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			for user in app_users:
				if user.get('U_ID') == uid:
					readlater = user.get('ReadLaterList')
					session['readlater_lock'] = True
					flash(readlater)
					return redirect(url_for('readlater'))

class UpdateReadLater(Resource):
	#http://127.0.0.1:5000/updatelink/0/'https://website.com/article.html'
	def get(self, uid, url): #page refers to the webpage to redirect to
		global app_users
		global app_files
		try:
		    uid = int(uid)
		except ValueError:
		    return "Please enter a valid U_ID (int)"
		else: 
			for user in app_users:
				if user.get('U_ID') == uid:
					query = {"U_ID": uid}
					url = unquote(url)
					updated_user = { "$pull": {
						'ReadLaterList': url,
					}}
					db.users_db.user_collection.update_one(query, updated_user)
					app_users, app_files = updateDB()
					session['readlater_lock'] = False
					flash("Article removed from your saved articles list.")
					return redirect(url_for('homepage'))

class SetNumFiles(Resource):	
	def post(self):
		num = request.form.get("file_num")
		try:
			num = int(num)
		except ValueError:
			return "Please enter an integer from 1-10." #Should be impossible unless messing with URL
		else:
			if (num < 1 or num > 10):
				return "Please enter an integer from 1-10." #Should be impossible unless messing with URL
			else:		
				session['num_files'] = num
				return redirect(url_for('upload'))																


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<uid>')
api.add_resource(FileList, '/files')
api.add_resource(File, '/files/<fid>/<method>')
api.add_resource(UserFiles, '/ufiles/<uid>/<page>') #used to get files by a user ID	
api.add_resource(Searcher, '/search/<query>') #used with newsfeed ingest to search
api.add_resource(SaveReadLater, '/savelink/<uid>/<url>') #used for read later feature in news analyzer
api.add_resource(LoadReadLater, '/loadlinks/<uid>') #used to retrieve read later links
api.add_resource(UpdateReadLater, '/updatelink/<uid>/<url>') #deleting a saved link
api.add_resource(SetNumFiles, '/setnumfiles')

if __name__ == '__main__':
    app.run(debug=True)
