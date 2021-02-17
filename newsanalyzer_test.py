#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# News Analyzer Testing
# ========================================================================

# ========================================================================
# Import newsanalyzer.py
# ========================================================================

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
uploadingCancelled = False
userID = "0" #Will implement user ID's with secure user authentication system
from newsanalyzer import *

# ========================================================================
# File Uploader/Ingest Testing
# ========================================================================

def test_UploadFiles():
	assert UploadFiles("1", files) == False
	#assert UploadFiles("0") == False
	assert UploadFiles("0", files) == True

def test_DisplayUploadStatus():
	assert DisplayUploadStatus(0) == True
	assert DisplayUploadStatus(50) == True
	assert DisplayUploadStatus(100) == True
	assert DisplayUploadStatus(200) == False
	assert DisplayUploadStatus(-1) == False

def test_RenderProgressBar():
	assert RenderProgressBar(True) == True
	assert RenderProgressBar(False) == True

def test_UploadError():
	assert UploadError("File1.txt") == "Alert to user: There was a problem uploading File1.txt"
	assert UploadError("File2.txt") == "Alert to user: There was a problem uploading File2.txt"

def test_CancelUpload():
	assert CancelUpload() == False

def test_FileDelete():	
	assert FileDelete("1", "Sample.txt") == False
	#assert FileDelete("0") == False
	assert FileDelete("0", "File.txt") == False
	assert FileDelete("0", "DONOTREAD.docx") == True

def test_FileEditName():
	assert FileEditName("1", "Sample.txt", "Example.txt") == False
	assert FileEditName("0", "Test.txt", "Testing.txt") == False
	assert FileEditName("0", "Sample.txt", "Example.txt") == "Example.txt"

def test_OrganizeFileList():
	assert OrganizeFileList("0", files, "Test") == False
	assert OrganizeFileList("1", files, "Alphabetical") == False
	assert OrganizeFileList("0", files, "Alphabetical") == ["DONOTREAD.docx", "Sample.txt", "WhiteHouseBriefing.pdf"]
	assert OrganizeFileList("0", files, "Reverse Alphabetical") == ["WhiteHouseBriefing.pdf", "Sample.txt", "DONOTREAD.docx"]
	assert OrganizeFileList("0", files, "Earliest Uploaded") == files
	assert OrganizeFileList("0", files, "Latest Uploaded") == files

# ========================================================================
# Text NLP Analysis Testing
# ========================================================================	

def test_ConvertFilesToText():
	assert ConvertFilesToText("1", files) == False
	assert ConvertFilesToText("0", files) == [["txt", "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."], ["docx", "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."], ["pdf", "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun."]]

def test_CreateKeywords():
	assert CreateKeywords("Placeholder") == ("The Earth is habitable in part due to its perfect distance from the Sun.", ["Sun", "Earth", "Solar System", "Planet", "Star"])

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

# ========================================================================
# Newsfeed Ingest Testing
# ========================================================================

def test_DiscoverContent():
	assert DiscoverContent("Placeholder") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]

def test_DisplayContent():
	assert DisplayContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]) == True

def test_OrganizeContent():
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Alphabetical") == (["https://en.wikipedia.org/wiki/Sun", "https://solarsystem.nasa.gov/solar-system/sun/overview/"], True)
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Latest Uploaded") == (["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], True)
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Most Relevant") == (["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], True)
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Something Else") == False

def test_ReadLater():
	assert ReadLater("1", "0010") == False
	assert ReadLater("0", "0001") == False
	assert ReadLater("0", "0010") == "0010"

# ========================================================================
# Logging and Diagnostics Testing
# ========================================================================

def test_SendLogReport():
	assert SendLogReport("ERROR: Upload Failure") == True

def test_Diagnostics():
	assert Diagnostics() == True
  
