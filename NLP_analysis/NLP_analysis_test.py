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
	test_files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf", "Operations.pdf"] #Sample list
	assert ConvertFileToText(10, test_files) == False
	assert ConvertFileToText(0, test_files) == [['txt', 'Testing123...'], ['docx', 'The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun.'], ['pdf', 'White House Briefing: Today on February 21.......\n'], ['pdf', 'Luke Staib: U39863533\n2\n-\n11\n-\n21\nEC500\nProfessor Osama\nHomework 2 Phase 1: Operations for the Secure File Uploader/Ingest, Text NLP Analysis, and \nNewsfeed Ingest\nSecure File Uploader/Ingest\n-\nAPI Type:\nEntity\n-\nbased\n-\nOperations:\no\nUploadFile\ns\n(userID, file\ns[]\n)\nWill upload\nwill change based on type of being uploaded\nFor multiple files, number of files in file \nlist\nwill determine how many \ntimes this function is ran\ni\nn a loop\nThis operation needs to be secure\no\nDisplay\nUpload\nStatus(\npercent\n)\nWill return progress of which files have been successfully uploaded\no\nRenderProgressBar(\nswitch\n)\nRenders and un\n-\nrenders progress bar based on upload status\no\nUploadError(file)\nShows \nwhich file caused an error while uploading\no\nCancelUpload()\nWill \ncancel current upload process\no\nFileDelete(\nuserID, \nfile)\nWill delete file from current list displayed (in \nlist\nfiles[])\no\nFileEditName(\nuserID, \nfile\n, new_name\n)\nWill allow user to change name of \nselected file\nto\na new n\name\no\nOrganizeFileList(files[]\n, organize_type\n)\nWill organize files[] array with several different options\nAlphabetical, Latest Uploaded, Earliest Uploaded, etc.\n-\nData:\no\nText \nd\nata: TXT, PPT, PPTX, RTF, PDF, DOC, DOCX, CSV, XLS, XLSM, \nXL\nSX\n, \netc\n.\no\nPotentially incorporate z\nipped \nd\nata: \nZIP, RAR, TAR, \n7Z\n, etc\n.\no\nWill handle large files, multiple files at once, etc.\no\nOnly articles, no multimedia\n(?)\n-\nStatus:\no\nBefore upload\nAPI gives o\nption to upload one file\nor\no\nDuring upload\nAPI s\nhows \nthe current \nstatus of \nthe \nupload, shows how many uploads \nhave been uploaded so far\nOption to cancel uploading mid\n-\nupload\no\nAfter\nsuccessful\nupload\nAPI d\nisplay\ns\nmessage to user that upload of files has b\neen completed \nsuccessfully\no\nError during upload process\nAPI displays any errors, lets user know that\nan\nerror occurred, \ndiscusses details of specific errors to the user regarding usage\nError information relayed in development logs\no\nFiles uploaded display\nWil\nWill be able to organize, delete, edit name o\nf\nfiles\nText NLP Analysis\n-\nAPI Type:\nProcedure\n-\nbased\n-\nOperations:\no\nConvertFilesToText(\nuserID, \nfiles[])\nConvert file data into TXT/JSON data \nto be used in text analysis such \nas Google NLP\no\nCreateKeywords\n(text\n)\n\nTakes in input from user and analyzes it using \nweb\n-\nbased data such as \nAPI data from many different news websites\n, generate keywords\no\nObtainArticles(\ntext\n)\nKeywords used from AssessData() will be used to obtain articles that \ndiscuss the topic that the text is discussing, obtaining relevant writing\no\nAssessData(article_data, keywords, text\n)\nThis is where the program will take all aspects, article data from \nObtai\nnArticles(), keywords from CreateKeywords(), and the original \ntext or file/s to create a sentiment\no\nSaveSentiment(userID, sentiment)\no\nEditSentiment(\nuserID, \nsentiment\n, new_sentiment\n)\nThis is \nwhere a user can edit a sentiment that the program generated\no\nDeleteSentiment(sentiment)\nA user can also delete a sentiment and try again with different \nparameters\no\nTranslate(tex\nt\n, language\n)\nTranslates text\nor sentiment\ninto different languages\nWill start wi\nth popular languages: English, Spanish, Chinese, \nFrench, Hindi, Portuguese,\nRussian, Japanese, German, \nDanish, etc.\n-\nData:\no\nText \ndata turned into TXT or JSON\n: TXT, PPT, PPTX, RTF, PDF, DOC, \nDOCX, CSV, XLS, XLSM, XLSX, ZIP, RAR, TAR, 7Z, etc.\no\nExtract data fro\nm other sources: Tweets, emails, reviews, social media posts, \netc.\n-\n> turn into TXT or JSON\no\nInput is converted into TXT or JSON to be analyzed by the system, outputted \nas TXT sentiment \n-\nStatus:\no\nT\nhe API will be used in a t\next\n-\ninput \ninterface\n:\nUser can enter\ntext or use uploaded files\n\nAPI \nwill show progress/status of text analysis\nAPI will display any errors\nthat occurred while analyzing text or files\nAPI\nwill show user sentiment that the system calculates based on the \ntext inputted\n, user is then able to\ntranslate, \nsave, edit, or delete report \ngenerated\nNewsfeed Ingest\n-\nAPI Type:\nEntity\n-\nbased\n-\nOperations:\no\nDiscoverContent(search_text)\nTakes in text that user enters to search for relevant information on that \ntopic, uses keywords in the \ntext entered\nUses NLP analysis\nor Google API\nto return specific articles\nReturns with relevant searches\no\nDisplayContent(\nsearches[]\n)\nAfter articles are foun\nd from the Internet, this command will \ndisplay\nthe specific articles\no\nOrganizeContent(\nsearches[], \norganize_type)\nAble to organize content that the program returns in different ways\nAlphabetical, Most Recent, Most \nRelevant\n(in terms of the \nresult of the NLP \noutput)\no\nReadLater(userID, articleID)\nAllows a user to save a specific article to their user account to read \nlate\nr\n-\nData:\no\nAPI takes in\ntext based data\n, entered in a text field for example\no\nAPI r\neturns a list of articles that a user can browse through\nor \nsave to read \nlater\n-\nStatus:\no\nAPI \nshows progress of \ncurrent \nsearch, then \ndisplays relevant \narticles \no\nAPI grants u\nser ab\ni\nl\nity\nto \norganize\narticles \nin a graphical user interface\n, \nAPI \ngrants \nuser\nability to\nsave articles \nto read later \nwith indicator that the \narticle \nhas been saved\nDiagnostic\nand Logging\nFunctions\n-\nSendLogReport(error)\no\nLogs the current process of the user to be used for debugging purposes, saves \n.log file or specific error triggered to database statistics file\no\nUses error types to organize types\nof errors, takes in an error as input\n-\nDiagnostics()\no\nProfiling discussed in class such as determining CPU usage, memory usage; \nshow traces, warnings, etc.\n']]
	# assert ConvertFilesToText(0, files) == [['txt', 'Testing123...'], ['docx', 'The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun.'], ['pdf', 'White House Briefing: Today on February 21.......\n']]
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
