#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# NLP Analysis
# ========================================================================

#I will create the website with Flask, I will use S3 or MongoDB for my database, I will use S3(?) to host

# ========================================================================
# Imports/Constants
# ========================================================================

import cProfile
import tracemalloc #Memory profiling
from tqdm import tqdm
import logging #Logging
import PyPDF2 #PDF -> TXT
#import docx2txt #DOC -> TXT

tracemalloc.start()

logging.basicConfig(filename='NLP_analysis.log', level=logging.DEBUG, format='%(levelname)s: %(message)s')

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
userID = "0" #Will implement user ID's with secure user authentication system

# ========================================================================
# Text NLP Analysis
# ========================================================================

def ConvertFilesToText(userID, files):
	if (userID != "0"):
		logging.error("User account with userID " + userID + " not found.")
		return False
	else:
		logging.info("User account with userID " + userID + " verified.")
		data_list = []
		for file in tqdm(files, total=len(files), desc="File Conversion Progress"):
			split_str = file.split(".")
			filename = split_str[0]
			filetype = split_str[1]
			filetype = filetype.lower()
			file_path = "./test_files/" + file
			if filetype == "docx":
				logging.debug("Here, I will use the docx2txt library to turn this .docx file into .txt")
				logging.info("Filetype = .docx")
				text_data = "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."	
			elif filetype == "txt":
				logging.debug("Here, there is no conversion to do since it is already a .txt file")
				logging.info("Filetype = .txt")
				file_ref = open(file_path, "r")
				text_data = file_ref.read()
				logging.debug("File contents: " + text_data)
			elif filetype == "pdf":
				logging.debug("Here, I will use the PyPDF2 library to turn this pdf file into .txt")
				logging.info("Filetype = .pdf")
				file_ref = open(file_path, "rb")
				file_reader = PyPDF2.PdfFileReader(file_ref)
				text_data = ""
				for i in range(file_reader.numPages):
					page = file_reader.getPage(i)
					text_data += page.extractText()
				file_ref.close()	
			else:
				logging.debug("I will implement support for other filetypes")
				logging.info("Filetype = other")	
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
	logging.info("Sentiment of text information entered: " + sentiment)
	return sentiment

def SaveSentiment(userID, sentiment):
	if (userID != "0"):
		logging.error("User account with userID " + userID + " not found.")
		return False
	else:
		logging.info("User account with userID " + userID + " verified.")
		#save sentiment to user ID sentiment[] list of strings in database
		logging.info("Sentiment \"" + sentiment + "\" saved.")
		return True

def EditSentiment(userID, sentiment, new_sentiment):
	if (userID != "0"):
		logging.error("User account with userID " + userID + " not found.")
		return False
	else:
		logging.info("User account with userID " + userID + " verified.")
		sentiments = ["The sky is yellow.", "The Sun is cold."]
		if sentiment in sentiments:
			for i, x in enumerate(sentiments):
				if x == sentiment:
					sentiments[i] = new_sentiment
			logging.info("Sentiment \"" + sentiment + "\" replaced with \"" + new_sentiment + "\".")
			return True		
		else:
			logging.info("Sentiment \"" + sentiment + "\" not found")
			return False	

def Translate(text, language):
	# use Google Translate API to take in text or sentiment and translate into any language in Google translate API
	# translated_text = GoogleTranslateAPI(text, language)
	if language == "English":
		translated_text = "Hello"
		logging.info("Text translated into English.")
	elif language == "Spanish":
		translated_text = "Hola"
		logging.info("Text translated into Spanish.")
	elif language == "Chinese":
		translated_text = "你好"
		logging.info("Text translated into Chinese.")
	elif language == "French":
		translated_text = "Bonjour"
		logging.info("Text translated into French.")
	else:
		logging.error("Unrecognized Language: " + language)
		return False			

	return translated_text	

def DiagnosticsNLP():
	#CPU usage:
	logging.info("[STATS] Memory Usage: Top 5 files allocating the most memory:")
	snapshot = tracemalloc.take_snapshot()
	top_stats = snapshot.statistics('lineno')
	for stat in top_stats[:5]:
	    logging.info(stat)

	#Memory usage:
	logging.info("[STATS] CPU Usage: Testing ConvertFilesToText()")
	#output = cProfile.run('ConvertFilesToText(str(0), files)')  #-> needs to be in main part, not in a function
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

print("To be completed...")
output = ConvertFilesToText("0", files)
print(output)
DiagnosticsNLP()
