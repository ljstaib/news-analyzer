#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# NLP Analysis Testing
# ========================================================================

# ========================================================================
# Import NLP_analysis.py
# ========================================================================

# uploadingCancelled = False
# userID = "0" #Will implement user ID's with secure user authentication system
from NLP_analysis import *

# ========================================================================
# Text NLP Analysis Testing
# ========================================================================	

def test_ConvertFileToText():
	assert ConvertFileToText(10, "test file txt", 'txt') == False
	#Sample.txt in test_files
	assert ConvertFileToText(0, "test file txt", 'txt') == "Testing123..."
	#Operations.pdf in test_files
	assert ConvertFileToText(0, "test file pdf", 'pdf') == "Luke Staib: U39863533 2 - 11 - 21 EC500 Professor Osama Homework 2 Phase 1: Operations for the Secure File Uploader/Ingest, Text NLP Analysis, and  Newsfeed Ingest Secure File Uploader/Ingest - API Type: Entity - based - Operations: o UploadFile s (userID, file s[] ) Will upload will change based on type of being uploaded For multiple files, number of files in file  list will determine how many  times this function is ran i n a loop This operation needs to be secure o Display Upload Status( percent ) Will return progress of which files have been successfully uploaded o RenderProgressBar( switch ) Renders and un - renders progress bar based on upload status o UploadError(file) Shows  which file caused an error while uploading o CancelUpload() Will  cancel current upload process o FileDelete( userID,  file) Will delete file from current list displayed (in  list files[]) o FileEditName( userID,  file , new_name ) Will allow user to change name of  selected file to a new n ame o OrganizeFileList(files[] , organize_type ) Will organize files[] array with several different options Alphabetical, Latest Uploaded, Earliest Uploaded, etc. - Data: o Text  d ata: TXT, PPT, PPTX, RTF, PDF, DOC, DOCX, CSV, XLS, XLSM,  XL SX ,  etc . o Potentially incorporate z ipped  d ata:  ZIP, RAR, TAR,  7Z , etc . o Will handle large files, multiple files at once, etc. o Only articles, no multimedia (?) - Status: o Before upload API gives o ption to upload one file or o During upload API s hows  the current  status of  the  upload, shows how many uploads  have been uploaded so far Option to cancel uploading mid - upload o After successful upload API d isplay s message to user that upload of files has b een completed  successfully o Error during upload process API displays any errors, lets user know that an error occurred,  discusses details of specific errors to the user regarding usage Error information relayed in development logs o Files uploaded display Wil Will be able to organize, delete, edit name o f files Text NLP Analysis - API Type: Procedure - based - Operations: o ConvertFilesToText( userID,  files[]) Convert file data into TXT/JSON data  to be used in text analysis such  as Google NLP o CreateKeywords (text )  Takes in input from user and analyzes it using  web - based data such as  API data from many different news websites , generate keywords o ObtainArticles( text ) Keywords used from AssessData() will be used to obtain articles that  discuss the topic that the text is discussing, obtaining relevant writing o AssessData(article_data, keywords, text ) This is where the program will take all aspects, article data from  Obtai nArticles(), keywords from CreateKeywords(), and the original  text or file/s to create a sentiment o SaveSentiment(userID, sentiment) o EditSentiment( userID,  sentiment , new_sentiment ) This is  where a user can edit a sentiment that the program generated o DeleteSentiment(sentiment) A user can also delete a sentiment and try again with different  parameters o Translate(tex t , language ) Translates text or sentiment into different languages Will start wi th popular languages: English, Spanish, Chinese,  French, Hindi, Portuguese, Russian, Japanese, German,  Danish, etc. - Data: o Text  data turned into TXT or JSON : TXT, PPT, PPTX, RTF, PDF, DOC,  DOCX, CSV, XLS, XLSM, XLSX, ZIP, RAR, TAR, 7Z, etc. o Extract data fro m other sources: Tweets, emails, reviews, social media posts,  etc. - > turn into TXT or JSON o Input is converted into TXT or JSON to be analyzed by the system, outputted  as TXT sentiment  - Status: o T he API will be used in a t ext - input  interface : User can enter text or use uploaded files  API  will show progress/status of text analysis API will display any errors that occurred while analyzing text or files API will show user sentiment that the system calculates based on the  text inputted , user is then able to translate,  save, edit, or delete report  generated Newsfeed Ingest - API Type: Entity - based - Operations: o DiscoverContent(search_text) Takes in text that user enters to search for relevant information on that  topic, uses keywords in the  text entered Uses NLP analysis or Google API to return specific articles Returns with relevant searches o DisplayContent( searches[] ) After articles are foun d from the Internet, this command will  display the specific articles o OrganizeContent( searches[],  organize_type) Able to organize content that the program returns in different ways Alphabetical, Most Recent, Most  Relevant (in terms of the  result of the NLP  output) o ReadLater(userID, articleID) Allows a user to save a specific article to their user account to read  late r - Data: o API takes in text based data , entered in a text field for example o API r eturns a list of articles that a user can browse through or  save to read  later - Status: o API  shows progress of  current  search, then  displays relevant  articles  o API grants u ser ab i l ity to  organize articles  in a graphical user interface ,  API  grants  user ability to save articles  to read later  with indicator that the  article  has been saved Diagnostic and Logging Functions - SendLogReport(error) o Logs the current process of the user to be used for debugging purposes, saves  .log file or specific error triggered to database statistics file o Uses error types to organize types of errors, takes in an error as input - Diagnostics() o Profiling discussed in class such as determining CPU usage, memory usage;  show traces, warnings, etc. "

def test_CreateKeywords():
	assert CreateKeywords("Placeholder") == (["The Earth is habitable in part due to its perfect distance from the Sun."], ["Sun", "Earth", "Solar System", "Planet", "Star"])

def test_ObtainArticles():
	assert ObtainArticles("Placeholder") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]

def test_AssessData():
	assert AssessData(["The Earth is habitable in part due to its perfect distance from the Sun."], ["Sun", "Earth", "Solar System", "Planet", "Star"], "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun.") == "The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets."

def test_SaveSentiment():
	assert SaveSentiment(10, "Placeholder") == False
	assert SaveSentiment(0, "Placeholder") == True

def test_EditSentiment():
	assert EditSentiment(10, "Placeholder", "New placeholder") == False
	assert EditSentiment(0, "Placeholder", "New placeholder") == False
	assert EditSentiment(0, "The sky is yellow.", "The sky is blue.") == True

def test_Translate():
	assert Translate("Hello, my name is Luke!", "Spanish") == "Hola"
	assert Translate("Hola, me llamo Luke!", "English") == "Hello"
	assert Translate("The sky is in fact blue.", "Chinese") == "你好"
	assert Translate("What is the meaning of life?", "French") == "Bonjour"
	assert Translate("Scurvy is caused by a deficiency in Vitamin C.", "Pirate Speak") == False
