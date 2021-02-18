#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Newsfeed Ingest
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
# Implementation
# ========================================================================	

# =========================================================================================
# Testing with Command Line (will move to Website using ex. Django, Flask, Heroku to host)
# =========================================================================================

print("To be completed...")
