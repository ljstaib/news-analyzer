#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# NLP Analysis
# Website created with Flask, MongoDB used for database, S3 used to host
# ========================================================================

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
import logging #Logging
import slate3k #PDF -> TXT
import os
import re
import docx2txt #DOC -> TXT

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/luke/Documents/Code/EC500/HW2+3/.keys/key.json"
from google.cloud import language

tracemalloc.start()

# files_db = files_collection.find()
# files = []
# for file in files_db:
# 	files.append(file)

logging.basicConfig(filename='NLP_analysis.log', level=logging.DEBUG, format='%(levelname)s: %(message)s')

# filenames = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf", "Operations.pdf"] #Sample list
UPLOAD_FOLDER = './File_Data'
# userID = "0" #Will implement user ID's with secure user authentication system

# ========================================================================
# Text NLP Analysis
# ========================================================================

def ConvertFileToText(userID, file_in, filetype):
	if not isinstance(userID, int):
		logging.info("ConvertFileToText: userID (U_ID) should be an integer.")
		return False
	if not isinstance(filetype, str):
		logging.info("ConvertFileToText: \"filetype\" should be a string.")	
		return False
	result = doesUserExist(userID)
	if (result):
		if file_in == "test file txt":
			file_ref = open("../test_files/Sample.txt", "r")
			text_data = file_ref.read()
			text_data = re.sub(r'\n +', '\n', text_data)
			text_data = re.sub(r'\n+', '\n', text_data)
			text_data = re.sub(r'\n', ' ', text_data)
			text_data = re.sub(r'\t', ' ', text_data)
			text_data = re.sub(r' +', ' ', text_data)
			text_data = re.sub(r':', ' ', text_data)
			text_data = re.sub(r'"', '\"', text_data)
			text_data = re.sub(r"'", '\'', text_data)
			return text_data

		if file_in == "test file pdf":
			file_path = "../test_files/WhiteHouseBriefing.pdf"
			text_data = ""
			with open(file_path, "rb") as f:
				text_data = slate3k.PDF(f)

			#Get rid of multiple newline characters
			text_data = str("".join(text_data))
			text_data = re.sub(r'\n +', '\n', text_data)
			text_data = re.sub(r'\n+', '\n', text_data)
			text_data = re.sub(r'\n', ' ', text_data)
			text_data = re.sub(r'\t', ' ', text_data)
			text_data = re.sub(r' +', ' ', text_data)
			text_data = re.sub(r':', ' ', text_data)
			text_data = re.sub(r'"', '\"', text_data)
			text_data = re.sub(r"'", '\'', text_data)
			return text_data

		if file_in == "test file docx":
			file_path = "../test_files/DONOTREAD.docx"
			text_data = docx2txt.process(file_path)
			text_data = re.sub(r'\n +', '\n', text_data)
			text_data = re.sub(r'\n+', '\n', text_data)
			text_data = re.sub(r'\n', ' ', text_data)
			text_data = re.sub(r'\t', ' ', text_data)
			text_data = re.sub(r' +', ' ', text_data)
			text_data = re.sub(r':', ' ', text_data)
			text_data = re.sub(r'"', '\"', text_data)
			text_data = re.sub(r"'", '\'', text_data)
			return text_data
			
		file_path = UPLOAD_FOLDER + "/" + file_in.filename
		if filetype == "docx":
			logging.info("Here, I use the docx2txt library to turn this .docx file into .txt")
			logging.info("Filetype = .docx")
			text_data = docx2txt.process(file_path)	
		elif filetype == "txt":
			logging.info("Here, there is no conversion to do since it is already a .txt file")
			logging.info("Filetype = .txt")
			file_ref = open(file_path, "r")
			text_data = file_ref.read()
		elif filetype == "pdf":
			logging.info("Here, I use the slate3k library to turn this .pdf file into .txt")
			logging.info("Filetype = .pdf")
			text_data = ""
			with open(file_path, "rb") as f:
				text_data = slate3k.PDF(f)
			text_data = str("".join(text_data))	
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
	
		text_data = re.sub(r'\n +', '\n', text_data)
		text_data = re.sub(r'\n+', '\n', text_data)
		text_data = re.sub(r'\n', ' ', text_data)
		text_data = re.sub(r'\t', ' ', text_data)
		text_data = re.sub(r' +', ' ', text_data)
		text_data = re.sub(r':', ' ', text_data)
		text_data = re.sub(r'"', '\"', text_data)
		text_data = re.sub(r"'", '\'', text_data)
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

def ObtainCategories(text_data):
	#use text_data to search for specific parts on Google
	#take information received to pull specific articles for CreateKeywords() to use to generate keywords
    client = language.LanguageServiceClient()
    document = language.Document(content=text_data, type_=language.Document.Type.PLAIN_TEXT)
    response = client.classify_text(request={'document': document})
    categories = response.categories

    result = {}

    for category in categories:
        result[category.name] = category.confidence

    if (result != {}):
    	return result
    else:
    	return "N/A"

	#article_links = ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
	#return article_links

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

#SaveAnalysis in app.py, in /file GET method=analyze
# def SaveAnalysis(file):
# 	text_data = file.get('Text')
# 	keywords = CreateKeywords(text_data)
# 	sentiment = AssessData(text_data)
# 	try:
# 		categories = ObtainCategories(text_data)
# 	except:
# 		categories = {}

# 	updated_file = { "$set": {
# 		'Sentiment': sentiment, 
# 		'Tags': {
# 			'Status': "Analyzed",
# 			'Keywords': keywords,
# 			'Categories': categories,
# 		}
# 	}}
# 	query = {"F_ID": file.get('F_ID')}
# 	return updated_file, query	

def DiagnosticsNLP():
	try:
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

# print(ConvertFileToText(0, "test file txt", "txt"))
# print(ConvertFileToText(0, "test file docx", "docx"))
# print(repr(ConvertFileToText(0, "test file pdf", "pdf")))

# keywords = CreateKeywords("The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.")
# print("Keywords:")
# for keyword in keywords:
# 	print(keyword)

# sentiment_results = AssessData("The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.")
# print(sentiment_results)
# for k, v in sentiment_results.items():
# 	print(f"{k}: {v}")

# category_results = ObtainCategories("Google Home enables users to speak voice commands to interact with services through the Home's intelligent personal assistant called Google Assistant. A large number of services, both in-house and third-party, are integrated, allowing users to listen to music, look at videos or photos, or receive news updates entirely by voice.")
# print("Category Results: ")
# print(category_results)
