#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# News Analyzer Testing
# ========================================================================

# ========================================================================
# Import newsfeed_ingest.py
# ========================================================================

# files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
# uploadingCancelled = False
# userID = "0" #Will implement user ID's with secure user authentication system
from newsfeed_ingest import *

# ========================================================================
# Newsfeed Ingest Testing
# ========================================================================

def test_DiscoverContent():
	assert DiscoverContent("Placeholder") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]

def test_DisplayContent():
	assert DisplayContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]) == True

def test_OrganizeContent():
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Alphabetical") == ["https://en.wikipedia.org/wiki/Sun", "https://solarsystem.nasa.gov/solar-system/sun/overview/"]
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Latest Uploaded") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Most Relevant") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Something Else") == False

def test_ReadLater():
	assert ReadLater(10, "0010") == False
	assert ReadLater(0, "0001") == False
	assert ReadLater(0, "0010") == "0010"
  