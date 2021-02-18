#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# File Uploader/Ingest
# ========================================================================

#I will use Django and Heroku to host or Flask, I will use S3 or MongoDB for my database

# ========================================================================
# Imports/Constants
# ========================================================================

import cProfile
import tracemalloc #Memory profiling

tracemalloc.start()

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
#uploadingCancelled = False
userID = "0" #Will implement user ID's with secure user authentication system

class ProgressBar:
	def __init__(self, percent):
		self.percent = percent

# ========================================================================
# File Uploader/Ingest
# ========================================================================

def UploadFiles(userID, files):
	#Inputs: userID is a string, files[] is a string list

	if (userID != "0"):
		print("User account not found.")
		return False
	else:	
		# while (CancelUpload() == False):
		percent_done = 0 #Used to tell user the progress of files being uploaded
		successes = 0 #Used to count successful uploads to calculate current percent
		DisplayUploadStatus(0) #Start progress bar at zero

		#Upload file on website made with Django and Heroku or Flask

		for file in files:
			print("Retrieved file " + str(file))
			split_str = file.split(".")
			filename = split_str[0]
			filetype = split_str[1]
			filetype = filetype.lower()
			print("Uploading file " + str(file) + " with name " + filename)
			uploadSuccess = True
			if (uploadSuccess):
				successes += 1
				percent_done = round(float(successes / len(files)), 2)
				DisplayUploadStatus(percent_done)
			else:
				UploadError(file)
				return False
			if (CancelUpload() == True):
				break

		if (CancelUpload() == True):
			print("Cancelling POST operation to database")
			print("Alert to user: Upload successfully cancelled.")
			return False
		else:				
			DisplayUploadStatus(100)
			return True

def DisplayUploadStatus(percent):
	if (percent >= 0 and percent <= 100):
		pbar = ProgressBar(0)
		if percent == 0:
			RenderProgressBar(True)
			print("Progress Bar: 0%")
		elif percent == 100:
			pbar.percent = 100
			RenderProgressBar(False)
			print("Progress Bar: 100%")
			print("Upload/s complete!")
		else:
			pbar.percent = percent
			print("Progress Bar: " + str(percent) + "%")

		return True	
	else:
		print("Progress must be 0-100%")
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

def UploadError(file):
	error = "Alert to user: There was a problem uploading " + file
	return error

def CancelUpload():
	uploadingCancelled = False
	if (uploadingCancelled):
		return True
	else:
		return False		

def FileDelete(userID, file):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:
		print("Retrieving files list from user with userID " + userID)
		if file in files:
			print("Deleting file " + file)
			success = True
			if success:
				print("File " + file + " was deleted successfully.")
				return True
			else:
				print("ERROR: File " + file + " was not deleted.")
				return False
		else:
			print("Files does not exist in user\'s library")
			return False		

def FileEditName(userID, file, new_name):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:
		print("Retrieving files list from user with userID " + userID)
		if file in files:
			print("Changing name of " + file + " to " + new_name)
			success = True
			if success:
				print("File " + file + " was edited successfully.")
				return new_name
			else:
				print("ERROR: File " + file + " could not be edited.")
				return False
		else:
			print("File not found")
			return False		

def OrganizeFileList(userID, files, organize_type):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:	
		print("Retrieving files list from user with userID " + userID)
		print("Current order of files: ")
		print(files)
		if organize_type == "Alphabetical":
			new_files = sorted(files, key=None)
			print("New order of files (" + organize_type +"): ")
			print(new_files)
		elif organize_type == "Reverse Alphabetical":
			new_files = sorted(files, key=None, reverse=True)
			print("New order of files (" + organize_type +"): ")
			print(new_files)
		elif organize_type == "Earliest Uploaded":
			print("Organized content by earliest uploaded")
			new_files = files
			print("New order of files (" + organize_type +"): ")
			print(new_files)
		elif organize_type == "Latest Uploaded":
			print("Organized content by latest uploaded")
			new_files = files
			print("New order of files (" + organize_type +"): ")
			print(new_files)
		else:
			return False	

	return new_files		

# ========================================================================
# Implementation
# ========================================================================	

# =========================================================================================
# Testing with Command Line (will move to Website using ex. Django, Flask, Heroku to host)
# =========================================================================================

print("To be completed...")
