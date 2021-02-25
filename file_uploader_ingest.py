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
from newsanalyzer_data import *

#Import libraries
import cProfile #CPU
import tracemalloc #Memory profiling
from tqdm import tqdm #Percent bar
import logging #Logging

tracemalloc.start()

logging.basicConfig(filename='file_uploader_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
uploadingCancelled = False
userID = "0" #Will implement user ID's with secure user authentication system

# class ProgressBar:
# 	def __init__(self, percent):
# 		self.percent = percent				

# ========================================================================
# File Uploader/Ingest
# ========================================================================

def UploadFiles(userID, files):
	#Inputs: userID is a string, files[] is a string list

	result = doesUserExist(userID)
	if (result):	
		for file in tqdm(files, total=len(files), desc="File Upload Progress"):
			#print("Retrieved file " + str(file))
			split_str = file.split(".")
			filename = split_str[0]
			filetype = split_str[1]
			filetype = filetype.lower()
			logging.info("Uploading file " + str(file) + " with name " + filename)
			uploadSuccess = True
			if (uploadSuccess):
				logging.info("File %s uploaded.", file)
			else:
				logging.error("Problem uploading %s", file)
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
			if (len(files) == 1):
				logging.info("Uploading of file " + files[0] + " completed!")
				print("Alert to user: Uploading of file " + files[0] + " completed!")
			else:
				file_list = str(files)[1:-1]
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

def FileDelete(userID, file):
	result = doesUserExist(userID)
	if (result):
		#print("Retrieving files list from user with userID " + userID)
		if file in files:
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

def FileEditName(userID, file, new_name):
	result = doesUserExist(userID)
	if (result):
		#print("Retrieving files list from user with userID " + userID)
		if file in files:
			logging.info("Changing name of " + file + " to " + new_name)
			success = True
			if success:
				logging.info("File " + file + " was edited successfully.")
				return new_name
			else:
				logging.error("ERROR: File " + file + " could not be edited.")
				return False
		else:
			logging.error("File " + file + " not found")
			return False	
	else:
		return False			

def OrganizeFileList(userID, files, organize_type):
	result = doesUserExist(userID)
	if (result):
		#print("Retrieving files list from user with userID " + userID)
		if (len(files) == 1):
			logging.warning("Only 1 file, there is nothing to sort.")
			return False
		else:
			file_list = str(files)[1:-1]
			logging.info("Current order of files: " + file_list)

		if organize_type == "Alphabetical":
			new_files = sorted(files, key=None)
		elif organize_type == "Reverse Alphabetical":
			new_files = sorted(files, key=None, reverse=True)
		elif organize_type == "Earliest Uploaded":
			print("Organized content by earliest uploaded")
			new_files = files
		elif organize_type == "Latest Uploaded":
			print("Organized content by latest uploaded")
			new_files = files
		else:
			return False

		new_file_list = str(new_files)[1:-1]
		logging.info("New order of files (" + organize_type +"): " + new_file_list)	
		return new_files
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

# print("To be completed...")
UploadFiles("0", files)
# DiagnosticsUploader()
