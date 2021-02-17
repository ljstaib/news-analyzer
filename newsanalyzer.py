#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# News Analyzer
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
		while (CancelUpload() == False):
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
# Text NLP Analysis
# ========================================================================

def ConvertFilesToText(userID, files):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:
		data_list = []
		for file in files:
			split_str = file.split(".")
			filename = split_str[0]
			filetype = split_str[1]
			filetype = filetype.lower()
			if filetype == "docx":
				print("Here, I will use the docx2txt library turn this docx file into text")
			elif filetype == "txt":
				print("Here, there is no conversion to do since it is already a .txt file")
			elif filetype == "pdf":
				print("I will figure out some way of converting PDF to TXT")
			else:
				print("Other filetype")	

			text_data = "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."	
			data_list.append([filetype, text_data])	
	
	return data_list

def CreateKeywords(text_data):	
	articles = ObtainArticles(text_data) #get articles/links using Google API 
	#article_data = extra relevant information gathered from the articles
	#use results -> names of Internet links/articles, to generate 5 keywords -> a list of 5 strings
	#some Google NLP function
	
	article_data = ["The Earth is habitable in part due to its perfect distance from the Sun."]
	keywords = ["Sun", "Earth", "Solar System", "Planet", "Star"]

	return article_data, keywords

def ObtainArticles(text_data):
	#use text_data to search for specific parts on Google
	#take information received to pull specific articles for CreateKeywords() to use to generate keywords

	article_links = ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
	return article_links

def AssessData(article_data, keywords, text_data):
	#use GoogleAPI, keywords, and original text_data to create a universal common sentiment
	sentiment = "The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets."
	print("Sentiment of text information entered: " + sentiment)
	return sentiment

def SaveSentiment(userID, sentiment):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:
		#save sentiment to user ID sentiment[] list of strings in database
		print("Sentiment \"" + sentiment + "\" saved.")
		return True

def EditSentiment(userID, sentiment, new_sentiment):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:
		sentiments = ["The sky is yellow.", "The Sun is cold."]
		if sentiment in sentiments:
			for i, x in enumerate(sentiments):
				if x == sentiment:
					sentiments[i] = new_sentiment
			print("Sentiment \"" + sentiment + "\" replaced with \"" + new_sentiment + "\".")
			return True		
		else:
			print("Sentiment not found")
			return False	

def Translate(text, language):
	# use Google Translate API to take in text or sentiment and translate into any language in Google translate API
	# translated_text = GoogleTranslateAPI(text, language)
	if language == "English":
		translated_text = "Hello"
	elif language == "Spanish":
		translated_text = "Hola"
	elif language == "Chinese":
		translated_text = "你好"
	elif language == "French":
		translated_text = "Bonjour"
	else:
		print("Unrecognized Language: " + language)
		return False			

	return translated_text		

# ========================================================================
# Newsfeed Ingest
# ========================================================================

def DiscoverContent(search_text):
	# Use NLP analysis from last section or Google Search API to retrieve relevant links
	# Organize by relevant searches returned by API
	# searches = NLP results (string list of links)
	searches = ObtainArticles(search_text)

	return searches

def DisplayContent(searches):
	print("Searches displayed: ")
	i = 0
	for search in searches:
		print("Search " + str(i) + ": " + search)
		i += 1
	#Command organizes searches[] and puts them into a web element to display on the screen
	return True

def OrganizeContent(searches, organize_type):	
	if organize_type == "Alphabetical":
		new_searches = sorted(searches, key=None)
		print("New order of searches (" + organize_type +"): ")
		print(new_searches)
	elif organize_type == "Latest Uploaded":
		print("Organized content by latest uploaded")
		new_searches = searches
		print("New order of searches (" + organize_type +"): ")
		print(new_searches)
	elif organize_type == "Most Relevant":
		print("Organized content by most relevant")
		new_searches = searches
		print("New order of searches (" + organize_type +"): ")
		print(new_searches)
	else:
		return False	

	if (DisplayContent(new_searches)):
		return new_searches, True
	else:
		return False	

def ReadLater(userID, articleID):
	if (userID != "0"):
		print("User account not found.")
		return False
	else:	
		#Save article to user ID database to read_later[] list by using its ID (has to be some ID in Google API)
		articles = ["Populating Mars", "Why the Sky is in Fact Orange.", "Americans Need One Thing Right Now: Free Biscuits."]
		articleIDs = ["0001", "0002", "0003"]
		if articleID in articleIDs:
			print("Article with ID " + articleID + " already exists in user\'s read later list")
			return False
		else:
			print("Article with ID " + articleID + " saved in user\'s read later list.")
			return articleID

# ========================================================================
# Logging and Diagnostics
# ========================================================================

def SendLogReport(error):
	# If error occurs, can use this function to track the current process of the user that led to the error,
	# ...save .log files to the database interface to analyze
	# ...mark by specific errors to analyze
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
