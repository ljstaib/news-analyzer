#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# News Analyzer
# ========================================================================

#I will use Flask to host, I will use AWS for my database

# ========================================================================
# Imports/Constants
# ========================================================================

# ========================================================================
# File Uploader/Ingest
# ========================================================================

def UploadFiles(userID, files[], filetype):
	Psuedocode below:

	Inputs: userID is a string, files[] is a string list, filetype is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
	else:	
		while (CancelUpload() == False):
			percent_done = 0 #Used to tell user the progress of files being uploaded
			successes = 0 #Used to count successful uploads to calculate current percent
			DisplayUploadStatus(0) #Start progress bar at zero

			Upload file on website made with Django and Heroku or Flask

			for file in files[]:
				retrieve file from computer of user
				trim file to save filename (remove extension for the name but save the filetype)
				upload specific file to database based on filetype variable
				if (upload is successful):
					successes += 1
					percent_done = round(float(successes / len(files)), 2)
					update DisplayUploadStatus(percent_done) to reflect progress
				else:
					UploadError(file) and show error, which file failed and why

		if (CancelUpload() == True):
			cancel POST uploading of files
			tell user operation was cancelled and exit
		else:				
			Call DisplayUploadStatus(100) to tell user that file uploading has been completed

def DisplayUploadStatus(percent):
	Psuedocode below:

	percent is a float

	if percent == 0:
		User must have just started so spawn progress bar: RenderProgressBar(True) 
		...this will be created with some web elements, not sure
		set the percent of the progress bar to zero
	elif percent == 100:
		Set progress bar to 100 percent
		Progress is done so RenderProgressBar(False)
		Display message that uploading has been completed
	else:
		In the middle of uploading files so just set the percent bar to the current percent	

def RenderProgressBar(switch):
	Psuedocode below:

	switch is a bool

	DisplayUploadStatus(percent) is used to update the number of the progress bar, 
	...this function is to just turn the render on and off 

	if (switch):
		if (progress bar is not there):
			use web elements to render the progress bar
	else:
		if (progress bar is there):
			use web elements to remove the progress bar	

def UploadError(file):
	Psuedocode below:

	file is a string

	print out a message telling the user that there was a problem uploading "file"
	describe what happened so user can change their behavior to have program running,
	...example: if they uploaded an unsupported file

def CancelUpload():
	Psuedocode below:

	This function is used in UploadFiles() to stop the current process if necessary

	if user hit cancel button, updates a global variable that sets to True:
		return True
	else:
		return False		

def FileDelete(userID, file):
	Psuedocode below:

	userID is a string, file is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
	else:
		retrieve user list files[] from database
		find file in user list files[]
		if file exists: (it should since user selected it from their list of files[])
			delete from that userID account on database
			if successful:
				tell file was deleted successfully
			else:
				display error to user

def FileEditName(userID, file, new_name):
	Psuedocode below:

	userID is a string, file is a string, new_name is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
	else:
		retrieve user list files[] from database
		find file in user list files[]
		if file exists: (it should since user selected it from their list of files[])
			edit name of file with new_name, update in database
			if successful:
				tell file name was edited successfully
			else:
				display error to user

def OrganizeFileList(files[], organize_type):
	Psuedocode below:

	files is a string list, organize_type is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
	else:	
		retrieve user list files[] from database
		shuffle indexes based on organize_type
		if organize_type == "Alphabetical":
			sort(list) in alphabetical order
		elif organize_type == "Reverse Alphabetical":
			sort(list) in reverse from alphabetical order
		elif organize_type == "Earliest Uploaded":
			sort(list) by earliest files under userID in database
		elif organize_type == "Latest Uploaded":
			sort(list) by latest files under userID in database
		can add more sorting methods
	
	update list display of files[] to user	

# ========================================================================
# Text NLP Analysis
# ========================================================================

def ConvertFilesToText(userID, files[]):
	Psuedocode below:

	userID is a string, files[] is a list of strings

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
		return False
	else:
		Take files and convert to TXT/JSON data (I will call text_data) using different methods depending on the filetype
		filetype = file extension by splitting string, taking text after decimal point "."
		filetype = filetype.lower()
		if filetype == "docx":
			then use the docx2txt library to retrieve text data
		etc. for other file types
	
	CreateKeywords(text_data)

def CreateKeywords(text_data):
	Psuedocode below:

	text_data is a string

	use text_data as search method for Google NLP API
	articles = ObtainArticles(text_data) to get articles/links using Google API 
	use results -> names of Internet links/articles, to generate 5 keywords -> a list of 5 strings
	article_data = extra relevant information gathered from the articles

	AssessData(article_data, keywords[], text_data)

def ObtainArticles(text_data):
	Psuedocode below:

	text_data is a string

	use text_data to search for specific parts on Google
	take information received to pull specific articles for CreateKeywords() to use to generate keywords

	return article_links

def AssessData(article_data[], keywords[], text_data):
	Psuedocode below:

	article_data is a string list(possibly), keywords is a string list, text_data is a string
	sentiment = use GoogleAPI, keywords, and original text_data to create a universal common sentiment

	display sentiment to user, allow them to save, edit, or delete and try again

def SaveSentiment(userID, sentiment):
	Psuedocode below

	userID is a string, sentiment is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
		return False
	else:
		save sentiment to user ID sentiment[] list of strings in database

def EditSentiment(userID, sentiment, new_sentiment):
	Psuedocode below:

	userID is a string, sentiment is a string, new_sentiment is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
	else:
		retrieve user list sentiments[] from database
		find sentiment in user list sentiments[]
		if sentiment exists: (it should since user selected it from their list of sentiments[] or changed it upon viewing immediately)
			edit sentiment with new_sentiment, update in database

def Translate(text or sentiment, language):
	Psuedocode below:

	text or sentiment is a string, language is a string

	use Google Translate API to take in text or sentiment and translate into any language in Google translate API
	translated_text = GoogleTranslateAPI(text, language)??

	return translated_text		


# ========================================================================
# Newsfeed Ingest
# ========================================================================

def DiscoverContent(search_text):
	Psuedocode below:

	search_text is a string

	Use NLP analysis from last section or Google Search API to retrieve relevant links
	Organize by relevant searches returned by API
	searches[] = NLP results (string list of links)

	return searches[]

def DisplayContent(searches[]):
	Psuedocode below:

	searches is a string list

	Command organizes searches[] and puts them into a web element to display on the screen

def OrganizeContent(searches[], organize_type):	
	Psuedocode below:

	searches is a string list, organize_type is a string

	shuffle indexes based on organize_type
		if organize_type == "Alphabetical":
			sort(list) in alphabetical order
		elif organize_type == "Latest Uploaded":
			sort(list) by latest searches by date
		elif organize_type == "Most Relevant":
			sort(list) by most relevant (aka back to default searches[])

	call DisplayContent(searches[]) to render new web element

def ReadLater(userID, articleID):
	Psuedocode below:

	userID is a string, articleID is a string

	Locate account with user ID:
	find(userID)
	if (userID does not exist in database):
		quit and show error("User ID not found or account not made, something to that effect")
	else:	
		Save article to user ID database to read_later[] list by using its ID (has to be some ID in Google API):

# ========================================================================
# Logging and Diagnostics
# ========================================================================

def SendLogReport(error):
	Psuedocode below:

	If error occurs, can use this function to track the current process of the user that led to the error,
	...save .log files to the database interface to analyze
	...mark by specific errors to analyze

	if error from UploadFiles():
		error_type = 1
	something like this

def Diagnostics():
	Psuedocode below:

	Profiling functions:
	I took these examples from additions I made to my homework 1
		CPU usage:
			print("[Top 5 files allocating the most memory:]")
			for stat in top_stats[:5]:
			    print(stat)

		Memory usage:
			print("[ANALYZING] int_float_check()")
			cProfile.run('int_float_check(10)')

		Network traffic usage and bandwidth usage

	Sends information to database interface		


# ========================================================================
# Implementation
# ========================================================================	

# =========================================================================================
# Testing with Command Line (will move to Website using ex. Django, Flask, Heroku to host)
# =========================================================================================