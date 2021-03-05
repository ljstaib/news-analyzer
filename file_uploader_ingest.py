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

#Import Data (in future from database)
from db import *

#Import libraries
import cProfile #CPU
import tracemalloc #Memory profiling
from tqdm import tqdm #Percent bar
import logging #Logging

tracemalloc.start()

logging.basicConfig(filename='file_uploader_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')

# files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
users = users_collection.find()
user_names = []
for user in users:
	user_names.append(user.get("U_ID"))
# print(user_names)	

files_db = files_collection.find()
files = []
for file in files_db:
	files.append(file)

uploadingCancelled = False		

# ========================================================================
# File Uploader/Ingest
# ========================================================================

def UploadFiles(userID, files_in):
	#Inputs: userID is a string, files[] is a string list

	result = doesUserExist(userID)
	if (result):
		filenames = []
		files_num = 0
		for file in files_in: #put tqdm back
			#print("Retrieved file " + str(file))
			files_num += 1
			print("File:")
			print(file)
			filename = file.get("Name")
			filenames.append(filename)
			filetype = file.get("Filetype")
			filetype = filetype.lower()
			logging.info("Uploading file " + str(filename + filetype) + " with name " + filename)
			uploadSuccess = True
			if (uploadSuccess):
				logging.info("File %s uploaded.", filename + filetype)
			else:
				logging.error("Problem uploading %s", filename + filetype)
				return False
			if (uploadingCancelled == True):
				break

		if (uploadingCancelled == True):
			logging.info("User requested to cancel upload.")
			logging.info("Cancelling POST operation to database.")
			logging.info("Upload successfully cancelled.")
			print("Alert to user: Upload successfully cancelled.")
			return False
		else:				
			if (files_num == 1):
				logging.info("Uploading of file " + filename + " completed!")
				print("Alert to user: Uploading of file " + filename + " completed!")
			else:
				file_list = str(filenames)[1:-1]
				logging.info("Uploading of files completed: " + file_list + "!")
				print("Alert to user: Uploading of files completed: " + file_list + "!")	
			return True	
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

def FileDelete(userID, fileID, files):
	result = doesUserExist(userID)
	if (result):
		fileExists = False
		saved_file = ""
		for file in files:
			if fileID == file.get("F_ID"):
				fileExists = True
				saved_file = str(file.get("Name"))
				break
		file = saved_file
		if (fileExists):
			logging.info("Deleting file " + file)
			success = True
			if success:
				logging.info("File " + file + " was deleted successfully.")
				return True
			else:
				logging.error("File " + file + " was not deleted.")
				return False
		else:
			logging.error("File " + file + " does not exist in user\'s library")
			return False
	else:
		return False				

def FileEditName(userID, fileID, files, new_name):
	result = doesUserExist(userID)
	fileExists = False
	if (result):
		#print("Retrieving files list from user with userID " + userID)
		for file in files:
			fid = file.get("F_ID")
			if (fid == fileID):
				fileExists = True
				filename = file.get("Name")
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
