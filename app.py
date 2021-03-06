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
from flask import Flask, flash, render_template, redirect, request, jsonify, make_response, url_for
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

#################################

app = Flask(__name__)
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

# @app.route('/test_db')
# def test_db():
# 	test_user = {
# 		'U_ID': 100, 
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
					updated_user = { "$set": {
						'Username': uname,
						'Password': pword, 
						'FirstName': fname, 
						'LastName': lname
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
			'LastName': new_lname
		}	
		db.users_db.user_collection.insert_one(new_user)
		app_users, app_files = updateDB()
		# new_user = (encodeJSON().encode(new_user)).replace(r'\"', '"')
		# new_user = json.JSONDecoder().decode(new_user)
		# app_users.append(new_user)
		return redirect(url_for("success"))

class File(Resource):
	#http://127.0.0.1:5000/files/0
	def get(self, fid):
		try:
		    fid = int(fid)
		except ValueError:
		    return "Please enter a valid F_ID (int)"
		else: 
			for file in app_files:
				if file.get('F_ID') == fid:
					return file
			return "F_ID does not exist"

	#curl http://127.0.0.1:5000/files/3 -X DELETE -v
	def delete(self, fid):
		try:
		    fid = int(fid)
		except ValueError:
		    return "Please enter a valid F_ID (int)"
		else: 
			global app_users
			global app_files
			for file in app_files:
				if file.get('F_ID') == fid:
					query = {"F_ID": fid}
					db.files_db.file_collection.delete_one(query)
					app_users, app_files = updateDB() 
					return f"Deleted file with F_ID: {fid}"
			return "F_ID does not exist"

	#curl http://127.0.0.1:5000/files/2 -d "FileInfo=WhiteHouseBriefing, PDF, Luke Staib, 1, 6264, Analyzed" -X PUT -v
	def put(self, fid): #edit info
		try:
		    fid = int(fid)
		except ValueError:
		    return "Please enter a valid F_ID (int)"
		else: 
			global app_users
			global app_files
			args = parser.parse_args()
			for file in app_files:
				if file.get('F_ID') == fid:
					query = {"F_ID": fid}
					fileinfo = list(args['FileInfo'].split(", "))
					if (len(fileinfo) != 6):
						return "To edit an existing file, FileInfo is a list of SIX arguments."
					filename = fileinfo[0]
					filetype = fileinfo[1]
					authors = fileinfo[2]
					source = fileinfo[3] #user who uploaded
					filesize = fileinfo[4]
					status = fileinfo[5]
					#Upload time and creation time have no reason to be touched
					updated_file = { "$set": {
						'Name': filename, 
						'Filetype': filetype, 
						'Authors': authors, 
						'Source': source,
						'Size': filesize,
						'Tags': {
							'Status': status,
						}
					}}
					db.files_db.file_collection.update_one(query, updated_file)
					app_users, app_files = updateDB()
					return updated_file
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
		fid = max_fid + 1

		if 'file' not in request.files:
			flash('No file part')
			return redirect("/")
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect("/")

		authors = request.form.get("authors")
		creation_time = str(request.form.get("month") + "/" + request.form.get("day") + "/" + request.form.get("year"))	
		new_file = UploadFiles(0, file, fid, authors, creation_time) #will incorporate userID auth 

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
			return f'There was a problem uploading your file.'
		else:	
			files_collection.insert_one(new_file)
			app_users, app_files = updateDB()
			return f'File uploaded successfully: {new_file}'	

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<uid>')
api.add_resource(FileList, '/files')
api.add_resource(File, '/files/<fid>')				

if __name__ == '__main__':
    app.run(debug=True)
