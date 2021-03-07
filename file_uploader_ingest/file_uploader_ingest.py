#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# File Uploader/Ingest
# ========================================================================

#I will create the website with Flask, I will use S3 or MongoDB for my database, I will use S3(?) to host

# ========================================================================
# Imports/Constants
# ========================================================================

#Import Data

#Import libraries
import cProfile #CPU
import tracemalloc #Memory profiling
from tqdm import tqdm #Percent bar
import logging #Logging
import os
from datetime import datetime

from werkzeug.utils import secure_filename

tracemalloc.start()

logging.basicConfig(filename='file_uploader_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')

UPLOAD_FOLDER = './File_Data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

import sys
sys.path.append('../')
from db import *
sys.path.append('../NLP_analysis')
from NLP_analysis import ConvertFileToText

# files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
# users = users_collection.find()
# user_names = []
# for user in users:
# 	user_names.append(user.get("U_ID"))
# # print(user_names)	

# files_db = files_collection.find()
# files = []
# for file in files_db:
# 	files.append(file)

app_users, app_files = updateDB()	

uploadingCancelled = False		

def allowed_file(filename):
	#Make sure file being uploaded is allowed
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========================================================================
# File Uploader/Ingest
# ========================================================================

def UploadFiles(userID, file_in, fid, authors, creation_time):
	#Inputs: userID is an int, file_in is a file object
	result = doesUserExist(userID)
	if (result):
		if file_in == "test_file": #for file_uploader_ingest_test.py, I can actually if files get uploaded using my website
			filename = "Test"
			filetype = "txt"
			text = "This is not a real file."
			source = 0
			filesize = 100
			status = "Testing file"
			upload_time = "1/1/1900"
			test_file = {
				'F_ID': fid, 
				'Name': filename, 
				'Filetype': filetype, 
				'Authors': authors,
				'Text': text,
				'CreationTime': creation_time,
				'Source': source,
				'Size': filesize,
				'UploadTime': upload_time,
				'Tags': {
					'Status': status,
				}
			}	
			return test_file
		else:	
			if file_in and allowed_file(file_in.filename):
				filename = secure_filename(file_in.filename)
				file_in.save(os.path.join(UPLOAD_FOLDER, filename))

				filename = file_in.filename
				filetype = file_in.filename.rsplit('.', 1)[1].lower()
				text = ConvertFileToText(0, file_in, filetype) #Working on this part next
				source = 0 #will assign userIDs when user auth is done
				filesize = os.stat(UPLOAD_FOLDER + "/" + filename).st_size
				status = "Uploaded"
				upload_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
				new_file = {
					'F_ID': fid, 
					'Name': filename, 
					'Filetype': filetype, 
					'Authors': authors,
					'Text': text,
					'CreationTime': creation_time,
					'Source': source,
					'Size': filesize,
					'UploadTime': upload_time,
					'Tags': {
						'Status': status,
					}
				}	
				logging.info("Uploading file " + str(filename))
				uploadSuccess = True
				if (uploadSuccess):
					logging.info("File %s uploaded.", filename + filetype)
				else:
					logging.error("Problem uploading %s", filename + filetype)
					return False
				if (uploadingCancelled == True): #might remove, cancelling uploads does not seem necessary
					return False
			else:
				return False			

		if (uploadingCancelled == True):
			logging.info("User requested to cancel upload.")
			logging.info("Cancelling POST operation to database.")
			logging.info("Upload successfully cancelled.")
			print("Alert to user: Upload successfully cancelled.")
			return False
		else:				
			logging.info("Uploading of file " + filename + " completed!")
			print("Alert to user: Uploading of file " + filename + " completed!")
			#files_collection.insert_one(new_file)
			return new_file
	else:
		return False		

def RenderProgressBar(switch):
	progressBarVisible = True
	if (switch):
		progressBarVisible = False
		if not progressBarVisible:
			print("Progress bar showing!")
	else:
		if (progressBarVisible):
			print("Progress bar not showing!")

	return True

def CancelUpload():
	uploadingCancelled = True
	return True	

def FileDelete(userID, fileID, file_in):
	result = doesUserExist(userID)
	if (result):
		fileExists = False
		if (file_in == "test_file"):
			return "I need to figure out how to test with a file object."
		saved_file = ""
		for file in files:
			if fileID == file_in.get("F_ID"):
				fileExists = True
				saved_file = str(file_in.get("Name"))
				break
		file_in = saved_file
		if (fileExists):
			logging.info("Deleting file " + file_in)
			success = True
			if success:
				logging.info("File " + file_in + " was deleted successfully.")
				return True
			else:
				logging.error("File " + file_in + " was not deleted.")
				return False
		else:
			logging.error("File " + file_in + " does not exist in user\'s library")
			return False
	else:
		return False				

def FileEditName(userID, fileID, file_in, new_name):
	result = doesUserExist(userID)
	if (result):
		fileExists = False
		if (file_in == "test_file"):
			return "I need to figure out how to test with a file object."
		#print("Retrieving files list from user with userID " + userID)
		for file_in in files:
			fid = file_in.get("F_ID")
			if (fid == fileID):
				fileExists = True
				filename = file_in.get("Name")
		if (fileExists):
			logging.info("Changing name of " + filename + " to " + new_name)
			success = True
			if success:
				logging.info("File " + filename + " was edited successfully.")
				return new_name
			else:
				logging.error("ERROR: File " + filename + " could not be edited.")
				return False
		else:
			logging.error("File " + filename + " not found")
			return False	
	else:
		return False			

def OrganizeFileList(userID, files, organize_type):
	result = doesUserExist(userID)
	if (result):
		if (files == "test_file"):
			return "I need to figure out how to test with a file object."
		#print("Retrieving files list from user with userID " + userID)
		files_num = 0
		filenames = []

		for file in files:
			files_num += 1
			filenames.append(file.get("Name"))

		if (files_num == 1):
			logging.warning("Only 1 file, there is nothing to sort.")
			return False
		else:
			file_list = str(filenames)[1:-1]
			logging.info("Current order of files: " + file_list)

		if organize_type == "Alphabetical":
			new_filenames = sorted(filenames, key=None)
		elif organize_type == "Reverse Alphabetical":
			new_filenames = sorted(filenames, key=None, reverse=True)
		elif organize_type == "Earliest Uploaded":
			print("Organized content by earliest uploaded")
			new_filenames = filenames
		elif organize_type == "Latest Uploaded":
			print("Organized content by latest uploaded")
			new_filenames = filenames
		else:
			return False

		new_file_list = str(new_filenames)[1:-1]
		logging.info("New order of files (" + organize_type +"): " + new_file_list)	
		return new_filenames
	else:
		return False		

def DiagnosticsUploader():
	#CPU usage:
	logging.info("[STATS] Memory Usage: Top 5 files allocating the most memory:")
	snapshot = tracemalloc.take_snapshot()
	top_stats = snapshot.statistics('lineno')
	for stat in top_stats[:5]:
	    logging.info(stat)

	#Memory usage:
	logging.info("[STATS] CPU Usage: Testing UploadFiles()")
	#output = cProfile.run('UploadFiles(str(0), files)')  #-> needs to be in main part, not in a function
	#logging.info(output)

	#Network traffic usage and bandwidth usage
	logging.info("[STATS] Analyzing traffic and bandwidth... to be implemented...")

	#Sends information to database interface	
	logging.info("[STATS] Sending diagnostic information to the database interface... to be implemented...")	
	return True		

# ========================================================================
# Implementation
# ========================================================================	

# =========================================================================================
# Testing with Command Line (will move to Website using ex. Django, Flask, Heroku to host)
# =========================================================================================

# test1 = UploadFiles(0, files)
# print(test1)
# test2 = OrganizeFileList(0, files, "Alphabetical")
# print(test2)
# test3 = FileDelete(0, 0, files)
# print(test3)
# test4 = FileEditName(0, 0, files, "Demo.txt")
# print(test4)
# DiagnosticsUploader()
