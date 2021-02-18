#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# NLP Analysis
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
# Implementation
# ========================================================================	

# =========================================================================================
# Testing with Command Line (will move to Website using ex. Django, Flask, Heroku to host)
# =========================================================================================

print("To be completed...")
