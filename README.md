# Homework #2 / Final Project for EC500 at BU: news-analyzer-ljstaib
## Please email me if there is a deliverable that you do not see (I should have everything completed), email me to host the web application. Also, please see a demonstration of how the website is used in "UsageExample.mp4" in the folder labeled "Final_Information".

Copyright @2021 
Luke Staib 
ljstaib@bu.edu

# Hosting information
- Website hosted at http://34.227.178.224:80/ (currently offline)

# Final Project Status
## Features to add/improve upon for my Final Project:
- [ ] Security
  - [ ] Encrypting user information and file information (?) for storage in MongoDB Atlas
  - [X] Ensuring file upload is secure
  - [X] Ability for a user to reset their password on the login screen
- [X] File Uploader
  - [X] Adding new types of files (RTF, ODT?)
  - [X] Ability to upload more than one file at once
- [X] NLP Analysis
  - [X] More thorough final sentiment and analysis based off of data received (if possible)
  - Additional features?
- [X] Newsfeed ingest
  - [X] Adding more than one website for articles (NYT)
  - [X] Adding "Read Later" feature, create "ReadLaterList" field for each user in database, read/edit this list
- [ ] Quality of Life Improvements
  - [ ] Loading icons
  - [X] Improved styling

## Status/Progress:
- Added newsapi.org API to gather articles from more websites (4/18)
  - Application gathers ~15 unique articles (only so many a flask session variable can hold) from newsapi.org and ~10 unique articles from NYT
- Finished "Read Later" feature (4/18-4/19)
  - User can save a link to their saved links on the newsfeed ingest screen
  - Can view their links from the homepage and read the article saved, or delete the link from their list
  - Updated style of page when no links are saved (4/21)
- Can now upload multiple files at once (4/19-4/20)
  - A user is able to upload 1-10 files instead of just 1 at a time
  - Added new HTML page: numfiles.html so that a user can select the number of files to upload at once
  - Incorporated a for loop in my upload code to retrieve file data for up to 10 files at a time
  - Limitation: Same authors, creation date for each file, but a user can edit this information when viewing a list of their files
- Can now upload .RTF files (4/21) 
- Made NLP analysis more clear to user (4/21)
  - Instead of score and magnitude, shows sentiment as negative, neutral, or positive and the magnitude as weakly expressed, strongly expressed, or in the middle
- NLP Overhaul (5/1)
  - I created a separate analysis screen that a user can access from the file menu
  - A user can click on the "View Analysis" corresponding to a specific article to take them to a separate page
  - NLP information is no longer crammed on the file list page
  - Begun working on code to summarize the text data of articles
- NLP continued (5/2)
  - Edited analysis page
  - Finished implementing summarization of inputted text (8 sentences)
- A user can now reset their password using the interface (5/3)
  - Created "resetpass.html"
  - Checks if passwords match, if password is from 8-256 characters, if user exists
- 5/4
  - Fixed bug with newsfeed analyzer that would cause searches to not show up
  - Improved styling on the home screen

# HW2 Status - HW2
Phase 1: Completed. Stub-API modules for Phase 1 are in their respective .py files. I also have psuedocode in newsanalyzer_pseudocode.txt.

Phase 2: Completed. Files and users database has been connected and GET, POST, PUT, DELETE operations are possible.

Phase 3: Completed. Please see NLP_analysis.py for the ConvertFilesToText() function. I can currently convert from TXT and PDF files. 2/25: Turned extra newline characters into only one for converted PDFs. Just need to modify the output a little bit.

Phase 3 Deliverable 1: Completed. Data storage defined in DataStorageStrategy.pdf. Code has started to be updated to incorporate MongoDB. Please see NewsAnalyzerDemo3_1.mov for a demonstration of my current API. Data is pulled from MongoDB.

Phase 3 Deliverable 2: Completed. Data being stored in database, can store text data of PDF files and TXT files. Created separate field "Text" in files database for each file. Please see "TextConversionWithFileUpload.mov" for my latest demo. Also please see "MongoDBFiles.png" for a view of the updated database.
- 3/14: I can now convert from DOCX to text

Hosting: I was able to get my website up on AWS EC2 on HTTP protocol

Queues (Mini Project): Completed. I made a demo program for subprocesses and multithreading. Please see my repository for more information: https://github.com/BUEC500C1/queues-ljstaib . 

My findings and what I have learned from the Queues Mini Project: 
- For less function calls, use multithreading, for more function calls, use multiprocessing if your machine has multiple CPU cores. However, with my demonstration files in my queues-ljstaib repository, I had greater success with function calls within my program than with multithreading or multiprocessing. I'm sure this is just something wrong I was doing on my end.
- I have learned how to use multiple threads and multiple processes to set a queue for functions. In my example, I created a prime numbers function and I reused the FileUploader() function from my code in this library. Utilizing queuing would be beneficial for my application if I have time to implement.

Week of 3/22: Completed.
- 3/19: User authentication, file uploader, and viewing of files fully functional on website.
- 3/21-3/22: Basic sentiment and keyword analysis implemented. Newsfeed ingest can take in a keyword to search the web.
- 3/23: File uploading, editing, deleting finalized. Upgraded PDF conversion. Added new webpages.
- 3/24-3/25: Finalized web application, finished NLP analysis, created newsfeed ingest using New York Times API
- 3/27: Web app completed, documentation written up and a demonstration of the application was created. Please see Final_Information.

# Phase 1:
Phase 1, due 2/15/21:

- Secure File Uploader/Ingest
- Text NLP Analysis
- Newsfeed Ingest

Extra Requirements:

- Create user stories for these APIs
- For each module, make a decision: Procedure-based or entity-based
- For each module, decide on operations, data and status
- Implement a stub-API
- Use Actions and unit test

# Phase 2:
- Use Flask as your WEB service platform
  - Reference 1: https://palletsprojects.com/p/flask/ (Github: https://github.com/pallets/flask )
  - Reference 2: Flask-RESTFUL (Github: https://github.com/flask-restful/flask-restful )
- Step 2: Integrate your module to become a RESTFUL system
  - Deploy your system to free AWS services: https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc
  - Develop simple WEB applications to test your system.
  - Document your REST APIs on your Github

# Phase 3:
- Focus on Ingestor module
- Investigate PDF to Text conversions
  - How to Extract Data from PDF Forms Using Python
  - pdfreader
  - Python for Pdf
  - PDFMiner
  - Fork of PDFMiner
  - Pdfplumber
- Chose module you want to use and implement uploader and Ingester
- For storage, use a folder. No need for cloud storage.
- For extracted text, store the data in files. No database yet.
- Due Date 2/28/2021. It is strict this time because we want to use the database concept and implement other modules.

- First Deliverable: Due Date: 3/1/2021
  - Setup mysql or MongoDB
  - Create your database (Tables in case of mysql or containers in case of MongoDB)
  - Define your data storage strategy

- Second Deliverable: Due Date: 3/7/2021
  - Extract Text from PDF files
  - Store Data in Database
  - Dates this time are strict because we want to use the database concept and implement other modules.

# Queues Mini Project
- Establish a processing criteria:
  - How many API calls you can handle simultaneously and why?
  - For example, run different API calls at the same time?
  - Split the processing of an API into multiple threads or processes?
- Recommendation for working on the homework:  
  - Step 1:
    - Develop a queue system that can exercise your requirements with stub functions.
  - Step 2:
    - Test it with different paramters
  - Include tracking interface to show how many processes are going on and success of each
- Due March 17th 2021
- Please see status for an explanation of my findings and what I have learned

# Week of 3/22
- Complete the file uploader
- Complete Sentiment analysis based on Google NLP. Make sure it runs on your machine.
- Complete newsfeed search section of application
