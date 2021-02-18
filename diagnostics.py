#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Diagnostics
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
# Logging and Diagnostics
# ========================================================================

def SendLogReport(error):
	# If error occurs, can use this function to track the current process of the user that led to the error,
	# ...save .log files to the database interface to analyze
	# ...mark by specific errors to analyze
	#Python logging
	print("[LOG] ERROR: " + error)
	print("[LOG] Sending log report...")
	return True

def Diagnostics():
	#CPU usage:
	print("[STATS] [Top 5 files allocating the most memory:]")
	snapshot = tracemalloc.take_snapshot()
	top_stats = snapshot.statistics('lineno')
	for stat in top_stats[:5]:
	    print(stat)

	#Memory usage:
	print("[STATS] Testing UploadFiles() for CPU usage")
	#cProfile.run('UploadFiles(0, files)') -> needs to be in main part, not in a function

	#Network traffic usage and bandwidth usage
	print("[STATS] Analyzing traffic and bandwidth... to be implemented...")

	#Sends information to database interface	
	print("[STATS] Sending diagnostic information to the database interface.")	
	return True

# ========================================================================
# Implementation
# ========================================================================	

# =========================================================================================
# Testing with Command Line (will move to Website using ex. Django, Flask, Heroku to host)
# =========================================================================================

print("To be completed...")
