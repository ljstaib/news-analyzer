#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# File Uploader/Ingest
# Website created with Flask, MongoDB used for database, S3 used to host
# ========================================================================

# ========================================================================
# Imports/Constants
# ========================================================================

#Import Data

#Import libraries
import cProfile #CPU
import tracemalloc #Memory profiling
import logging #Logging
import os
import psutil
import time
from datetime import datetime

from werkzeug.utils import secure_filename

tracemalloc.start()

try:
	logging.basicConfig(filename='./file_uploader_ingest/file_uploader_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')
except FileNotFoundError:
	logging.basicConfig(filename='file_uploader_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')

UPLOAD_FOLDER = './File_Data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'rtf'}

import sys
sys.path.append('/home/runner/work/news-analyzer-ljstaib/news-analyzer-ljstaib')
sys.path.append('../')
from db import *

sys.path.append('./NLP_analysis')
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

def allowed_file(filename):
	#Make sure file being uploaded is allowed
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========================================================================
# File Uploader/Ingest
# ========================================================================

def UploadFiles(userID, file_in, fid, authors, creation_time):
	#Inputs: userID is an int, file_in is a file object, fid is an int, authors and creation time are strings from the website
	if not isinstance(userID, int):
		logging.warning("UploadFiles: user ID (U_ID) should be an integer")
		return False
	if not isinstance(fid, int):
		logging.warning("UploadFiles: file ID (F_ID) should be an integer")
		return False
	if not isinstance(authors, str):
		logging.warning("UploadFiles: \"authors\" should be a string")
		return False
	if not isinstance(creation_time, str):
		logging.warning("UploadFiles: \"creation_time\" should be a string")
		return False

	result = doesUserExist(userID)
	if (result):
		if file_in == "test_file": #for file_uploader_ingest_test.py
			filename = "Test"
			filetype = "txt"
			text = "This is not a real file."
			source = "test"+str(userID)
			filesize = -1
			status = "Testing file"
			upload_time = "1/1/1900"
			sentiment = None
			keywords = None
			categories = None
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
				'Sentiment': sentiment,
				'Tags': {
					'Status': status,
					'Keywords': keywords,
					'Categories': categories,
				}
			}	
			return test_file
		else:	
			if file_in and allowed_file(file_in.filename):
				filename = secure_filename(file_in.filename)
				file_in.save(os.path.join(UPLOAD_FOLDER, filename))

				filename = file_in.filename
				filetype = file_in.filename.rsplit('.', 1)[1].lower()
				text = ConvertFileToText(userID, file_in, filetype)
				if text == False:
					text = ""
				source = userID
				filesize = os.stat(UPLOAD_FOLDER + "/" + filename).st_size
				upload_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
				sentiment = None
				status = "Uploaded"
				keywords = None
				categories = None
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
					'Sentiment': sentiment,
					'Tags': {
						'Status': status,
						'Keywords': keywords,
						'Categories': categories,
					}
				}	
				logging.info("Uploading file " + str(filename))
				return new_file
			else:
				return False			
	else:
		return False		

# def RenderProgressBar(switch):
# 	progressBarVisible = True
# 	if (switch):
# 		progressBarVisible = False
# 		if not progressBarVisible:
# 			print("Progress bar showing!")
# 	else:
# 		if (progressBarVisible):
# 			print("Progress bar not showing!")

# 	return True

# def CancelUpload():
# 	uploadingCancelled = True
# 	return True	

def FileDelete(fileID): #revamped to work with app.py
	if not (isinstance(fileID, int)):
		logging.warning("FileDelete(): File ID (F_ID) should be an integer")
		return False
	if (fileID == -1):
		logging.info("Testing FileDelete()")
		return False
	try:
		query = {"F_ID": fileID} 
		files_collection.delete_one(query)
		return True
	except:
		return False					

def FileEdit(fileID, authors, creation_time): #revamped to work with app.py, will add more things to edit
	if not (isinstance(fileID, int)):
		logging.warning("FileDelete(): File ID (F_ID) should be an integer")
		return False
	if not (isinstance(authors, str)):
		logging.warning("FileDelete(): \"authors\" should be a string")
		return False
	if not (isinstance(creation_time, str)):
		logging.warning("FileDelete(): \"creation_time\" should be a string")
		return False
	if (fileID == -1):
		logging.info("Testing FileEdit()")
		return False	

	try:
		query = {"F_ID": fileID}
		updated_file = { "$set": { 
			'Authors': authors, 
			'CreationTime': creation_time,
		}}
		files_collection.update_one(query, updated_file)
		return True
	except:
		return False				

#Will implement after newsfeed ingest if time

# def OrganizeFileList(userID, files, organize_type):
# 	result = doesUserExist(userID)
# 	if (result):
# 		if (files == "test_file"):
# 			return "I need to figure out how to test with a file object."
# 		#print("Retrieving files list from user with userID " + userID)
# 		files_num = 0
# 		filenames = []

# 		for file in files:
# 			files_num += 1
# 			filenames.append(file.get("Name"))

# 		if (files_num == 1):
# 			logging.warning("Only 1 file, there is nothing to sort.")
# 			return False
# 		else:
# 			file_list = str(filenames)[1:-1]
# 			logging.info("Current order of files: " + file_list)

# 		if organize_type == "Alphabetical":
# 			new_filenames = sorted(filenames, key=None)
# 		elif organize_type == "Reverse Alphabetical":
# 			new_filenames = sorted(filenames, key=None, reverse=True)
# 		elif organize_type == "Earliest Uploaded":
# 			print("Organized content by earliest uploaded")
# 			new_filenames = filenames
# 		elif organize_type == "Latest Uploaded":
# 			print("Organized content by latest uploaded")
# 			new_filenames = filenames
# 		else:
# 			return False

# 		new_file_list = str(new_filenames)[1:-1]
# 		logging.info("New order of files (" + organize_type +"): " + new_file_list)	
# 		return new_filenames
# 	else:
# 		return False		

def DiagnosticsUploader():
	try:
		#CPU usage:
		logging.info("[STATS] Memory Usage: Top 5 files allocating the most memory:")
		snapshot = tracemalloc.take_snapshot()
		top_stats = snapshot.statistics('lineno')
		for stat in top_stats[:5]:
		    logging.info(stat)

		#Memory usage:
		logging.info("[STATS] CPU Usage: Testing FileDelete()")
		#output = cProfile.run('FileDelete(100)')  #-> needs to be in main part, not in a function
		#logging.info(output)

		#Network traffic usage and bandwidth usage
		logging.info("[STATS] Analyzing bandwidth over 1 second")
		now1 = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
		time.sleep(1)
		now2 = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
		bwidth = ((now2 - now1) / 1024 / 1024 / 1024 * 8) #from bytes to gigabits
		if (bwidth > 0.02):
			logging.info(f'High amount of bandwidth used: {bwidth}')
		else:
			logging.info(f'Bandwidth used: {bwidth}')
		return True	
	except:
		return False		

# =========================================================================================
# Testing with Command Line
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
