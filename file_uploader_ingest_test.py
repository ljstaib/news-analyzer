#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# File Uploader/Ingest Testing
# ========================================================================

# ========================================================================
# Import file_uploader_ingest.py
# ========================================================================

files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
# uploadingCancelled = False
# userID = "0" #Will implement user ID's with secure user authentication system
from file_uploader_ingest import *

# ========================================================================
# File Uploader/Ingest Testing
# ========================================================================

def test_UploadFiles():
	assert UploadFiles(10, files) == False
	#assert UploadFiles("0") == False
	assert UploadFiles(0, files) == True

def test_RenderProgressBar():
	assert RenderProgressBar(True) == True
	assert RenderProgressBar(False) == True

def test_CancelUpload():
	assert CancelUpload() == True

def test_FileDelete():	
	assert FileDelete(10, 0, files) == False
	#assert FileDelete("0") == False
	assert FileDelete(0, 0, files) == True

def test_FileEditName():
	assert FileEditName(10, 0, files, "Example.txt") == False
	assert FileEditName(0, 0, files, "Example.txt") == "Example.txt"

def test_OrganizeFileList():
	assert OrganizeFileList(0, files, "Test") == False
	assert OrganizeFileList(10, files, "Alphabetical") == False
	assert OrganizeFileList(0, files, "Alphabetical") == ["DONOTREAD.docx", "Sample.txt", "WhiteHouseBriefing.pdf"]
	assert OrganizeFileList(0, files, "Reverse Alphabetical") == ["WhiteHouseBriefing.pdf", "Sample.txt", "DONOTREAD.docx"]
	assert OrganizeFileList(0, files, "Earliest Uploaded") == ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"]
	assert OrganizeFileList(0, files, "Latest Uploaded") == ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"]
