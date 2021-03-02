#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Flask Restful Website
# ========================================================================

#import modules
from file_uploader_ingest import *
from NLP_analysis import *
from newsfeed_ingest import *
import db

#flask, flask_restful
from flask import Flask, render_template, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource

#MongoDB JSON encoder
import json
from bson import ObjectId

from datetime import datetime

#################################

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app) 

class encodeJSON(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ObjectId):
			return str(obj)	
		return json.JSONEncoder.default(self, obj)

parser = reqparse.RequestParser()
parser.add_argument('UserInfo') 
parser.add_argument('FileInfo')
app_users = []
app_files = []			

def updateDB():
	#Download and convert data from users database
	data_users = users_collection.find()
	app_users = []
	for user in data_users:
		app_users.append(user)
	app_users = (encodeJSON().encode(app_users)).replace(r'\"', '"')
	app_users = json.JSONDecoder().decode(app_users)

	#Download and convert data from files database
	data_files = files_collection.find()
	app_files = []
	for file in data_files:
		app_files.append(file)
	app_files = (encodeJSON().encode(app_files)).replace(r'\"', '"')
	app_files = json.JSONDecoder().decode(app_files)
	return app_users, app_files	 		 

app_users, app_files = updateDB()

@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')

@app.route('/test_db')
def test_db():
	test_user = {
		'U_ID': 100, 
		'Username': "mongodb", 
		'FirstName': "Data", 
		'LastName': "Base"
	}
	db.users_db.user_collection.insert_one(test_user)	
	return "Uploaded test user to MongoDB!"	

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
			return "F_ID does not exist"						

class UserList(Resource):
	#http://127.0.0.1:5000/users
	def get(self):
		return app_users

	#curl http://127.0.0.1:5000/users -d "UserInfo=ljs123, Luke, Staib" -X POST -v
	#Right now, in order: username, first name, last name
	#then check GET method
	def post(self):
		global app_users
		global app_files
		args = parser.parse_args()
		# print(args)
		max_uid = 0
		for user in app_users:
			if user.get('U_ID') > max_uid:
				max_uid = user.get('U_ID')
		new_uid = max_uid + 1
		new_userinfo = list(args['UserInfo'].split(", "))
		# print(new_userinfo)
		new_uname = new_userinfo[0]
		new_fname = new_userinfo[1]
		new_lname = new_userinfo[2]
		new_user = {
			'U_ID': new_uid, 
			'Username': new_uname, 
			'FirstName': new_fname, 
			'LastName': new_lname
		}	
		db.users_db.user_collection.insert_one(new_user)
		app_users, app_files = updateDB()
		# new_user = (encodeJSON().encode(new_user)).replace(r'\"', '"')
		# new_user = json.JSONDecoder().decode(new_user)
		# app_users.append(new_user)
		return f'User uploaded successfully: {new_user}'

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

class FileList(Resource):
	#http://127.0.0.1:5000/files
	def get(self):
		return app_files

	#curl http://127.0.0.1:5000/files -d "FileInfo=FileName1, TXT, John Doe, 01/02/1980 00:00:00, 0, 100, Uploaded" -X POST -v
	#then check GET method
	def post(self):
		global app_users
		global app_files
		args = parser.parse_args()
		# print(args)
		max_fid = 0
		for file in app_files:
			if file.get('F_ID') > max_fid:
				max_fid = file.get('F_ID')
		fid = max_fid + 1
		new_fileinfo = list(args['FileInfo'].split(", "))
		print(new_fileinfo)
		filename = new_fileinfo[0]
		filetype = new_fileinfo[1]
		authors = new_fileinfo[2]
		creation_time = new_fileinfo[3]
		source = new_fileinfo[4]
		filesize = new_fileinfo[5]
		status = new_fileinfo[6]
		upload_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
		new_file = {
			'F_ID': fid, 
			'Name': filename, 
			'Filetype': filetype, 
			'Authors': authors, 
			'CreationTime': creation_time,
			'Source': source,
			'Size': filesize,
			'UploadTime': upload_time,
			'Tags': {
				'Status': status,
			}
		}	
		files_collection.insert_one(new_file)
		app_users, app_files = updateDB()
		return f'File uploaded successfully: {new_file}'	

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<uid>')
api.add_resource(FileList, '/files')
api.add_resource(File, '/files/<fid>')				

if __name__ == '__main__':
    app.run(debug=True)
