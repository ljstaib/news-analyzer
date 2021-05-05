#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Newsfeed Ingest
# Website created with Flask, MongoDB used for database, S3 used to host
# ========================================================================

# ========================================================================
# Imports/Constants
# ========================================================================

#Import Data (in future from database)
import sys
sys.path.append('/home/runner/work/news-analyzer-ljstaib/news-analyzer-ljstaib')
sys.path.append('../')
from db import *

#Import libraries
import cProfile
import tracemalloc #Memory profiling
import time
import psutil
import logging #Logging
import requests #retrieving articles
import newsapi #newsapi.org
import datetime #get dates for newsapi

tracemalloc.start()

for key in keys_collection.find():
	if (key.get('name') == "NYT"):
		nyt_key = key.get('key')
	elif (key.get('name') == "NewsAPI"):
		news_key = key.get('key')

users = users_collection.find()

logging.basicConfig(filename='newsfeed_ingest.log', level=logging.INFO, format='%(levelname)s: %(message)s')	

# ========================================================================
# Newsfeed Ingest
# ========================================================================

#Helper function used to retrieve dates for the newsapi.org search (searching within last month)
def get_dates():
	today = datetime.date.today()
	last_month = today
	if (today.month == 1):
		last_month.replace(month=12)
	else:	
		last_month.replace(month=today.month - 1)

	return last_month, today	

def DiscoverContent(search_text):
	# Use NLP analysis from New York Times API
	# Organize by relevant searches returned by API

	if not (isinstance(search_text, str)):
		logging.warning("Entered search text is not a string.")
		return False
	else:
		search_text = search_text.lower()
		logging.info("Search text is " + str(search_text))

		result_titles = [] #List of 25 titles to display
		result_urls = [] #List of 25 URLs to display
		result_sources = [] #List of 25 Sources to display
		results = [] #List of 3 lists above
		#15 results from newsapi.org, 10 results from new york times

		date_last_month, date_now = get_dates()
		news = None
		news = newsapi.NewsApiClient(api_key=news_key)
		#search wide variety of websites for content within the last month, 15 results because of size to hold in flash variable
		some_articles = news.get_everything(q=search_text, from_param=date_last_month, to=date_now, language='en', page=1)
		#print(some_articles)
		all_articles = some_articles.get('articles')
		article_titles = []
		articles = []
		for article in all_articles:
			if article.get('title') not in article_titles:
				article_titles.append(article.get('title'))
				articles.append(article)

		some_articles = articles[:15] #1st 15 results
		#print("SOME ARTICLES")
		#print(some_articles)

		for article in some_articles:
			result_titles.append(article.get('title'))
			result_urls.append(article.get('url'))
			result_sources.append(article.get('source').get('name'))

		#10 results
		url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + search_text + "&page=1" + "&api-key=" + nyt_key
		reqs = (requests.get(url)).json()
		#print(reqs)

		for i in range(1, len(reqs.get('response').get('docs'))):
			#print(reqs[j].get('response').get('docs')[i])
			#print('='*80)
			result_titles.append(reqs.get('response').get('docs')[i].get('snippet'))
			result_urls.append(reqs.get('response').get('docs')[i].get('web_url'))
			result_sources.append(reqs.get('response').get('docs')[i].get('source'))

		results = [result_titles, result_urls, result_sources]
		logging.info("Successful retrieval of news articles!")
		return results

# Handled in app.py
# def DisplayContent(searches):
# 	logging.info("Searches displayed: ")
# 	i = 0
# 	for search in searches:
# 		logging.info("Search " + str(i) + ": " + search)
# 		i += 1
# 	#Command organizes searches[] and puts them into a web element to display on the screen
# 	return True


# This function is not needed
# def OrganizeContent(searches, organize_type):	
# 	if (len(searches) == 1):
# 		logging.warning("Only 1 search result, there is nothing to organize.")
# 		return False
# 	else:
# 		search_list = str(searches)[1:-1]
# 		logging.info("First 20 searches: " + search_list[:20])

# 	if organize_type == "Alphabetical":
# 		new_searches = sorted(searches, key=None)
# 	elif organize_type == "Latest Uploaded":
# 		print("Organized content by latest uploaded")
# 		new_searches = searches
# 	elif organize_type == "Most Relevant":
# 		print("Organized content by most relevant")
# 		new_searches = searches
# 	else:
# 		return False		

# 	if (DisplayContent(new_searches)):
# 		new_search_list = str(new_searches)[1:-1]
# 		logging.info("New order of searches (" + organize_type +"): " + new_search_list)
# 		return new_searches
# 	else:
# 		return False	

# Not enough time for this feature
# def ReadLater(userID, articleID):
# 	result = doesUserExist(userID)
# 	if (result):
# 		#Save article to user ID database to read_later[] list by using its ID
# 		articles = ["Populating Mars", "Why the Sky is in Fact Orange.", "Americans Need One Thing Right Now: Free Biscuits."]
# 		articleIDs = ["0001", "0002", "0003"]
# 		if articleID in articleIDs:
# 			logging.error("Article with ID " + articleID + " already exists in user\'s read later list")
# 			return False
# 		else:
# 			logging.info("Article with ID " + articleID + " saved in user\'s read later list.")
# 			return articleID
# 	else:
# 		return False		

def DiagnosticsNewsfeed():
	try:
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

# results = DiscoverContent("election", 0) #Page 0 for results 1-10
# print(results)
# test = ReadLater(0, "0004")
# print(test)
# DiagnosticsNewsfeed()
