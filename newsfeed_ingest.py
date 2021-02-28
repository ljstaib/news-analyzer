#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Newsfeed Ingest
# ========================================================================

#I will create the website with Flask, I will use S3 or MongoDB for my database, I will use S3(?) to host

# ========================================================================
# Imports/Constants
# ========================================================================

#Import Data (in future from database)
from db import *

#Import libraries
import cProfile
import tracemalloc #Memory profiling
import logging #Logging

tracemalloc.start()

users = users_collection.find()

logging.basicConfig(filename='newsfeed_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')

# ========================================================================
# Newsfeed Ingest
# ========================================================================

def DiscoverContent(search_text):
	# Use NLP analysis from last section or Google Search API to retrieve relevant links
	# Organize by relevant searches returned by API
	# searches = NLP results (string list of links)
	# searches = ObtainArticles(search_text)
	searches = ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]

	return searches

def DisplayContent(searches):
	logging.info("Searches displayed: ")
	i = 0
	for search in searches:
		logging.info("Search " + str(i) + ": " + search)
		i += 1
	#Command organizes searches[] and puts them into a web element to display on the screen
	return True

def OrganizeContent(searches, organize_type):	
	if (len(searches) == 1):
		logging.warning("Only 1 search result, there is nothing to organize.")
		return False
	else:
		search_list = str(searches)[1:-1]
		logging.info("First 20 searches: " + search_list[:20])

	if organize_type == "Alphabetical":
		new_searches = sorted(searches, key=None)
	elif organize_type == "Latest Uploaded":
		print("Organized content by latest uploaded")
		new_searches = searches
	elif organize_type == "Most Relevant":
		print("Organized content by most relevant")
		new_searches = searches
	else:
		return False		

	if (DisplayContent(new_searches)):
		new_search_list = str(new_searches)[1:-1]
		logging.info("New order of searches (" + organize_type +"): " + new_search_list)
		return new_searches
	else:
		return False	

def ReadLater(userID, articleID):
	result = doesUserExist(userID)
	if (result):
		#Save article to user ID database to read_later[] list by using its ID (has to be some ID in Google API)
		articles = ["Populating Mars", "Why the Sky is in Fact Orange.", "Americans Need One Thing Right Now: Free Biscuits."]
		articleIDs = ["0001", "0002", "0003"]
		if articleID in articleIDs:
			logging.error("Article with ID " + articleID + " already exists in user\'s read later list")
			return False
		else:
			logging.info("Article with ID " + articleID + " saved in user\'s read later list.")
			return articleID
	else:
		return False		

def DiagnosticsNewsfeed():
	#CPU usage:
	logging.info("[STATS] Memory Usage: Top 5 files allocating the most memory:")
	snapshot = tracemalloc.take_snapshot()
	top_stats = snapshot.statistics('lineno')
	for stat in top_stats[:5]:
	    logging.info(stat)

	#Memory usage:
	logging.info("[STATS] CPU Usage: Testing DiscoverContent()")
	#output = cProfile.run('DiscoverContent(str(0))')  #-> needs to be in main part, not in a function
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
# result = DiscoverContent("Our Sun")
# print(result)
# test = ReadLater(0, "0004")
# print(test)
# DiagnosticsNewsfeed()
