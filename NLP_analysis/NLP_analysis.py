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

#Import Data (in future from database)
import sys
#Sys line below is so that the program works in GitHub Actions testing
sys.path.append('/home/runner/work/news-analyzer-ljstaib/news-analyzer-ljstaib')
sys.path.append('../')
from db import *

#Import libraries
import cProfile
import tracemalloc #Memory profiling
from tqdm import tqdm
import logging #Logging
import PyPDF2 #PDF -> TXT
import os
import re
import docx2txt #DOC -> TXT

from google.cloud import language

tracemalloc.start()

# files_db = files_collection.find()
# files = []
# for file in files_db:
# 	files.append(file)

logging.basicConfig(filename='NLP_analysis.log', level=logging.DEBUG, format='%(levelname)s: %(message)s')

filenames = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf", "Operations.pdf"] #Sample list
UPLOAD_FOLDER = './File_Data'
# userID = "0" #Will implement user ID's with secure user authentication system

# ========================================================================
# Text NLP Analysis
# ========================================================================

def ConvertFileToText(userID, file_in, filetype):
	result = doesUserExist(userID)
	if (result):
		# data_list = []
		# path_created = True
		# for file in tqdm(files, total=len(files), desc="File Conversion Progress"):
			# split_str = file.split(".")
			# filename = split_str[0]
			# filetype = split_str[1]
			# filetype = filetype.lower()
		if file_in == "test file txt":
			file_ref = open("./test_files/Sample.txt", "r")
			text_data = file_ref.read()
			return text_data

		if file_in == "test file pdf":
			file_ref = open("./test_files/Operations.pdf", "rb")
			file_reader = PyPDF2.PdfFileReader(file_ref)
			page_data = ""
			text_data = ""
			for i in range(file_reader.numPages):
				page = file_reader.getPage(i)
				page_data = page.extractText()
				#Get rid of multiple newline characters
				page_data = re.sub(r'\n +', '\n', page_data)
				page_data = re.sub(r'\n+', '\n', page_data)
				page_data = re.sub(r'\n', ' ', page_data)
				text_data += page_data
			file_ref.close()	
			return text_data
			
		file_path = UPLOAD_FOLDER + "/" + file_in.filename
		if filetype == "docx":
			logging.debug("Here, I use the docx2txt library to turn this .docx file into .txt")
			logging.info("Filetype = .docx")
			text_data = docx2txt.process(file_path)	
			logging.debug("File contents: " + text_data)
		elif filetype == "txt":
			logging.debug("Here, there is no conversion to do since it is already a .txt file")
			logging.info("Filetype = .txt")
			file_ref = open(file_path, "r")
			text_data = file_ref.read()
			logging.debug("File contents: " + text_data)
		elif filetype == "pdf":
			logging.debug("Here, I use the PyPDF2 library to turn this pdf file into .txt")
			logging.info("Filetype = .pdf")
			file_ref = open(file_path, "rb")
			file_reader = PyPDF2.PdfFileReader(file_ref)
			page_data = ""
			text_data = ""
			for i in range(file_reader.numPages):
				page = file_reader.getPage(i)
				page_data = page.extractText()
				#Get rid of multiple newline characters
				page_data = re.sub(r'\n +', '\n', page_data)
				page_data = re.sub(r'\n+', '\n', page_data)
				page_data = re.sub(r'\n', ' ', page_data)
				text_data += page_data
			file_ref.close()	
			logging.debug("File contents: " + text_data)
		else:
			logging.debug("I will implement support for other filetypes")
			logging.info("Filetype = other")	
			text_data = "Placeholder text for an unsupported file. Supported files are currently txt, pdf, docx."	


			# try:
			# 	os.mkdir("File_Data")
			# except FileExistsError:
			# 	logging.info("File directory for uploading files already exists.")
			# except OSError:
			# 	logging.error("Creation of file directory for uploading files failed.")
			# 	path_created = False
			# else:
			# 	logging.info("File directory for uploading files created.")

			# if (path_created):
			# 	fullname = os.path.join("./File_Data/", filename)
			# 	new_file = open(fullname, "w")
			# 	new_file.write(text_data)
			# 	new_file.close()

			# data_list.append([filetype, text_data])	
	
		return text_data
	else:
		return False		

def CreateKeywords(text_data): 
	#articles = ObtainArticles(text_data) #get articles/links using Google API 
	#article_data = extra relevant information gathered from the articles
	#use results -> names of Internet links/articles, to generate 5 keywords -> a list of 5 strings
	#some Google NLP function
	client = language.LanguageServiceClient()
	document = language.Document(content=text_data, type_=language.Document.Type.PLAIN_TEXT)

	response = client.analyze_entities(document=document)
	keywords = []
	for entity in response.entities:
		keywords.append(entity.name)
	
	#article_data = ["The Earth is habitable in part due to its perfect distance from the Sun."]
	#keywords = ["Sun", "Earth", "Solar System", "Planet", "Star"]
	logging.info("Keywords of text entered:")
	for k in keywords:
		logging.info("\t" + k)

	return keywords

def ObtainArticles(text_data):
	#use text_data to search for specific parts on Google
	#take information received to pull specific articles for CreateKeywords() to use to generate keywords

	article_links = ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
	return article_links

def AssessData(text_data):
	#use text_data to create a sentiment
	#sentiment = "The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets."

	client = language.LanguageServiceClient()
	document = language.Document(content=text_data, type_=language.Document.Type.PLAIN_TEXT)

	response = client.analyze_sentiment(document=document)

	sentiment = response.document_sentiment
	results = dict(
		text=text_data,
		score=f"{sentiment.score:.1%}",
		magnitude=f"{sentiment.magnitude:.1%}",
	)

	logging.info("Sentiment of text information entered: " + str(sentiment))
	return results

def SaveSentiment(userID, sentiment):
	result = doesUserExist(userID)
	if (result):
		#save sentiment to user ID sentiment[] list of strings in database
		logging.info("Sentiment \"" + sentiment + "\" saved.")
		return True
	else:
		return False	

def EditSentiment(userID, sentiment, new_sentiment):
	result = doesUserExist(userID)
	if (result):
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
	else:
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

# print("To be completed...")
# test1 = ConvertFilesToText(0, filenames)
# print(test1)
# test2 = SaveSentiment(0, "Sentiment")
# print(test2)
# test3 = EditSentiment(0, "The sky is yellow.", "The sky is blue.")
# print(test3)
# DiagnosticsNLP()

keywords = CreateKeywords("The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.")
print("Keywords:")
for keyword in keywords:
	print(keyword)

sentiment_results = AssessData("The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.")
print(sentiment_results)
for k, v in sentiment_results.items():
	print(f"{k}: {v}")
