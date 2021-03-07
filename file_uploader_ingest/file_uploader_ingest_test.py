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
	#UploadFiles(userID, file_in, fid, authors, creation_time)
	assert UploadFiles(10, "test_file", 1000, "Luke Staib", "3/6/21") == False
	assert UploadFiles(0, "test_file", 1000, "Luke Staib", "3/6/21") == {'F_ID': 1000, 'Name': "Test", 'Filetype': "txt", 'Authors': "Luke Staib",'Text': "This is not a real file.", 'CreationTime': "3/6/21", 'Source': 0, 'Size': 100, 'UploadTime': "1/1/1900", 'Tags': { 'Status': "Testing file", } }

def test_RenderProgressBar():
	assert RenderProgressBar(True) == True
	assert RenderProgressBar(False) == True

def test_CancelUpload():
	assert CancelUpload() == True

def test_FileDelete():	
	assert FileDelete(10, 0, "test_file") == False
	#assert FileDelete("0") == False
	assert FileDelete(0, 0, "test_file") == "I need to figure out how to test with a file object."
	#Need to add new testing!

def test_FileEditName():
	assert FileEditName(10, 0, "test_file", "Example.txt") == False
	assert FileEditName(0, 0, "test_file", "Example.txt") == "I need to figure out how to test with a file object."
	#Need to add new testing!

def test_OrganizeFileList():
	assert OrganizeFileList(10, "test_file", "Alphabetical") == False
	assert OrganizeFileList(0, "test_file", "Alphabetical") == "I need to figure out how to test with a file object."
	# assert OrganizeFileList(0, files, "Alphabetical") == ["DONOTREAD.docx", "Sample.txt", "WhiteHouseBriefing.pdf"]
	# assert OrganizeFileList(0, files, "Reverse Alphabetical") == ["WhiteHouseBriefing.pdf", "Sample.txt", "DONOTREAD.docx"]
	# assert OrganizeFileList(0, files, "Earliest Uploaded") == ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"]
	# assert OrganizeFileList(0, files, "Latest Uploaded") == ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"]
	#Need to add new testing!
