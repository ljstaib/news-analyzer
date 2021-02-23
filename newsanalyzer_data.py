#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# Data (until I use a database)
# ========================================================================
import logging #Logging

users = [
	{
		'U_ID': 0,
		'Username': "ljstaib",
		'FirstName': "Luke",
		'LastName': "Staib",
	},
	{
		'U_ID': 1,
		'Username': "johndoe",
		'FirstName': "John",
		'LastName': "Doe",
	}
]
#F_ID: File ID
#FileSize in bytes
#FileSource is U_ID of uploader
files = [
	{
		'F_ID': 0,
		'Name': 'Sample',
		'Filetype': 'TXT',
	 	'Authors': "Luke Staib",
		'CreationTime': "02/23/2021 14:40:57",
		'Source': 0,
		'Size': 13,
		'UploadTime': "02/23/2021 14:40:57",
		'Tags': {
			'Status': 'Uploaded',
	 	},
	},
	{
		'F_ID': 1,
		'Name': 'DONOTREAD',
		'Filetype': 'DOCX',
	 	'Authors': "Luke Staib",
		'CreationTime': "02/23/2021 14:40:57",
		'Source': 0,
		'Size': 11690,
		'UploadTime': "02/23/2021 14:40:57",
		'Tags': {
			'Status': 'Uploaded',
	 	},
	},
	{ #For this example, I made this document but "John Doe" uploaded it
		'F_ID': 2,
		'Name': 'WhiteHouseBriefing',
		'Filetype': 'PDF',
	 	'Authors': "Luke Staib",
		'CreationTime': "02/23/2021 14:40:57",
		'Source': 1,
		'Size': 6264,
		'UploadTime': "02/23/2021 14:40:57",
		'Tags': {
			'Status': 'Uploaded',
	 	},
	},
]
text = [
	{
		'T_ID': 0,
		'Text': "The Sun is the star at the center of our Solar System. Earth is the third closest planet to the Sun.",
		'Sentiment': "The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.",
		'NLP': {
			'Status': 'NotAnalyzed',
		},
	},
]

# ========================================================================
# Helper Functions
# ========================================================================			

def doesUserExist(uid):
	valid_user = False
	for user in users:
		for key, value in user.items():
			if key == "U_ID":
				logging.debug("User ID: " + str(value))
				if str(value) == str(uid):
					valid_user = True
	if not valid_user:
		logging.error("User account with userID " + str(uid) + " not found.")
		return False
	else:
		logging.info("User account with userID " + str(uid) + " verified.")
		return True	