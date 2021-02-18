#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Diagnostic Testing
# ========================================================================

# ========================================================================
# Import diagnostics.py
# ========================================================================

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
uploadingCancelled = False
userID = "0" #Will implement user ID's with secure user authentication system
from diagnostics import *

# ========================================================================
# Logging and Diagnostics Testing
# ========================================================================

def test_SendLogReport():
	assert SendLogReport("ERROR: Upload Failure") == True

def test_Diagnostics():
	assert Diagnostics() == True
  