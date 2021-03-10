#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Flask Restful Website
# ========================================================================

from flask import Flask
from flask_pymongo import pymongo
import logging

connection_url = open("mongo_url.txt", "r").read()
client = pymongo.MongoClient(connection_url)

users_db = client['Users']
users_collection = users_db['user_collection']

files_db = client['Files']
files_collection = files_db['file_collection']

text_db = client['Text']
text_collection = text_db['text_collection']

# ========================================================================
# Helper Functions
# ========================================================================

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