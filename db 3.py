#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Flask Restful Website
# ========================================================================

from flask import Flask
from flask_pymongo import pymongo
import logging

import json
from bson import ObjectId

connection_url = open("mongo_url.txt", "r").read()
client = pymongo.MongoClient(connection_url)

users_db = client['Users']
users_collection = users_db['user_collection']

files_db = client['Files']
files_collection = files_db['file_collection']

text_db = client['Text']
text_collection = text_db['text_collection']

# ========================================================================
# Helper Functions/Classes
# ========================================================================

class encodeJSON(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ObjectId):
			return str(obj)	
		return json.JSONEncoder.default(self, obj)

def doesUserExist(uid):
	valid_user = False
	users = users_collection.find()
	for user in users:
		for key, value in user.items():
			if key == "U_ID":
				logging.debug("User ID: " + str(value))
				if str(value) == str(uid):
					valid_user = True
	if not valid_user:
		logging.error("User account with userID " + str(uid) + " not found.")
		return False
	else:
		logging.info("User account with userID " + str(uid) + " verified.")
		return True	

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