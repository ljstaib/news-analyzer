#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# NLP Analysis Testing
# ========================================================================

# ========================================================================
# Import NLP_analysis.py
# ========================================================================

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
uploadingCancelled = False
userID = "0" #Will implement user ID's with secure user authentication system
from NLP_analysis import *

# ========================================================================
# Text NLP Analysis Testing
# ========================================================================	

def test_ConvertFilesToText():
	assert ConvertFilesToText("1", files) == False
	assert ConvertFilesToText("0", files) == [["txt", "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."], ["docx", "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."], ["pdf", "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."]]

def test_CreateKeywords():
	assert CreateKeywords("Placeholder") == (["The Earth is habitable in part due to its perfect distance from the Sun."], ["Sun", "Earth", "Solar System", "Planet", "Star"])

def test_ObtainArticles():
	assert ObtainArticles("Placeholder") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]

def test_AssessData():
	assert AssessData(["The Earth is habitable in part due to its perfect distance from the Sun."], ["Sun", "Earth", "Solar System", "Planet", "Star"], "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun.") == "The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets."

def test_SaveSentiment():
	assert SaveSentiment("1", "Placeholder") == False
	assert SaveSentiment("0", "Placeholder") == True

def test_EditSentiment():
	assert EditSentiment("1", "Placeholder", "New placeholder") == False
	assert EditSentiment("0", "Placeholder", "New placeholder") == False
	assert EditSentiment("0", "The sky is yellow.", "The sky is blue.") == True

def test_Translate():
	assert Translate("Hello, my name is Luke!", "Spanish") == "Hola"
	assert Translate("Hola, me llamo Luke!", "English") == "Hello"
	assert Translate("The sky is in fact blue.", "Chinese") == "你好"
	assert Translate("What is the meaning of life?", "French") == "Bonjour"
	assert Translate("Scurvy is caused by a deficiency in Vitamin C.", "Pirate Speak") == False
