#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# NLP Analysis Testing
# ========================================================================

# ========================================================================
# Import NLP_analysis.py
# ========================================================================

from NLP_analysis import *

# ========================================================================
# Text NLP Analysis Testing
# ========================================================================	

def test_ConvertFileToText():
	assert ConvertFileToText(10, "test file txt", 'txt') == False
	assert ConvertFileToText("test", "test file txt", 'txt') == False
	assert ConvertFileToText(10, "test file txt", 1) == False
	#Sample.txt in test_files
	assert ConvertFileToText(0, "test file txt", 'txt') == "Testing123..."
	# in test_files
	assert ConvertFileToText(0, "test file pdf", 'pdf') == "White House Briefing  Today on February 21....... \x0c"
	#DONOTREAD.docx in test_files
	assert ConvertFileToText(0, "test file docx", 'docx') == "Top secret! Your eyes only...."

#List of keywords is randomized every run so testing is never consistent
# def test_CreateKeywords():
# 	assert CreateKeywords("The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.") == ""

#Google Cloud API will not work with GitHub Action Testing
# def test_AssessData():
# 	assert AssessData("The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.") == {'text': 'The Sun is a yellow dwarf star at the center of our Solar System. The distance between the Sun and the Earth is one important reason why life can be sustained on Earth. At about 92 million miles away, the Earth is the third closest planet from the Sun out of 8 planets.', 'score': '0.0%', 'magnitude': '50.0%'}

#Google Cloud API will not work with GitHub Action Testing
# def test_ObtainCategories():
# 	assert ObtainCategories("Google Home enables users to speak voice commands to interact with services through the Home's intelligent personal assistant called Google Assistant. A large number of services, both in-house and third-party, are integrated, allowing users to listen to music, look at videos or photos, or receive news updates entirely by voice.") == {'/Computers & Electronics/Software': 0.550000011920929, '/Internet & Telecom': 0.5099999904632568}

# ========================================================================	

# Did not end up needing SaveSentiment or EditSentiment
# def test_SaveSentiment():
# 	assert SaveSentiment(10, "Placeholder") == False
# 	assert SaveSentiment(0, "Placeholder") == True

# def test_EditSentiment():
# 	assert EditSentiment(10, "Placeholder", "New placeholder") == False
# 	assert EditSentiment(0, "Placeholder", "New placeholder") == False
# 	assert EditSentiment(0, "The sky is yellow.", "The sky is blue.") == True

# Ran out of time
# def test_Translate():
# 	assert Translate("Hello, my name is Luke!", "Spanish") == "Hola"
# 	assert Translate("Hola, me llamo Luke!", "English") == "Hello"
# 	assert Translate("The sky is in fact blue.", "Chinese") == "你好"
# 	assert Translate("What is the meaning of life?", "French") == "Bonjour"
# 	assert Translate("Scurvy is caused by a deficiency in Vitamin C.", "Pirate Speak") == False

def test_DiagnosticsNLP():
	assert DiagnosticsNLP() == True

test_ConvertFileToText()
test_AssessData()
test_ObtainCategories()
test_DiagnosticsNLP()	