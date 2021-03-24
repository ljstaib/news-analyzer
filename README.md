# Homework #2 for EC500 at BU: news-analyzer-ljstaib

Copyright @2021 
Luke Staib 
ljstaib@bu.edu

# Status 
Phase 1: Completed. Stub-API modules for Phase 1 are in their respective .py files. I also have psuedocode in newsanalyzer_pseudocode.txt.

Phase 2: Completed. Files and users database has been connected and GET, POST, PUT, DELETE operations are possible.

Phase 3: Completed. Please see NLP_analysis.py for the ConvertFilesToText() function. I can currently convert from TXT and PDF files. 2/25: Turned extra newline characters into only one for converted PDFs. Just need to modify the output a little bit.

Phase 3 Deliverable 1: Completed. Data storage defined in DataStorageStrategy.pdf. Code has started to be updated to incorporate MongoDB. Please see NewsAnalyzerDemo3_1.mov for a demonstration of my current API. Data is pulled from MongoDB.

Phase 3 Deliverable 2: Completed. Data being stored in database, can store text data of PDF files and TXT files. Created separate field "Text" in files database for each file. Please see "TextConversionWithFileUpload.mov" for my latest demo. Also please see "MongoDBFiles.png" for a view of the updated database.
- 3/14: I can now convert from DOCX to text

Hosting: I was able to get my website up on AWS EC2 on HTTP protocol (might need to change to HTTPS)

Queues (Mini Project): In progress. I made a demo program for subprocesses and multithreading. Please see my repository for more information: https://github.com/BUEC500C1/queues-ljstaib . 

My findings and what I have learned from the Queues Mini Project: 
- For less function calls, use multithreading, for more function calls, use multiprocessing if your machine has multiple CPU cores. However, with my demonstration files in my queues-ljstaib repository, I had greater success with function calls within my program than with multithreading or multiprocessing. I'm sure this is just something wrong I was doing on my end.
- I have learned how to use multiple threads and multiple processes to set a queue for functions. In my example, I created a prime numbers function and I reused the FileUploader() function from my code in this library. Utilizing queuing would be beneficial for my application if I have time to implement.

Week of 3/22: In progress.
- 3/19: User authentication, file uploader, and viewing of files fully functional on website.
- 3/21-3/22: Basic sentiment and keyword analysis implemented. Newsfeed ingest can take in a keyword to search the web.
- 3/23: File uploading, editing, deleting finalized. Upgraded PDF conversion. Added new webpages.

TODO:
- Add more testing, GitHub issues
- Add NLP analysis to website

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
