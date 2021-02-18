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
uploadingCancelled = False
userID = "0" #Will implement user ID's with secure user authentication system
from file_uploader_ingest import *

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
