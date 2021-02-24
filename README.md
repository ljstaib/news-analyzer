# Homework #2 for EC500 at BU: news-analyzer-ljstaib

Copyright @2021 
Luke Staib 
ljstaib@bu.edu

Status:
--------------------------------------------------------------------------------------------------------------------------------

Phase 1: Completed. Stub-API modules for Phase 1 are in their respective .py files. I also have psuedocode in newsanalyzer_pseudocode.txt.

Phase 2: In progress. Working on integrating my modules to be a RESTFUL system. Currently I have made a simple website that you can add and look at a sample users and files list.

Phase 3: In progress. Please see NLP_analysis.py for the ConvertFilesToText() function. I can currently convert from TXT and PDF files.

Phase 1:
--------------------------------------------------------------------------------------------------------------------------------

Phase 1, due 2/15/21:
  - Secure File Uploader/Ingest
  - Text NLP Analysis
  - Newsfeed Ingest

Extra Requirements:
  - Create user stories for these APIs
  - For each module, make a decision:  Procedure-based or entity-based
  - For each module, decide on operations, data and status
  - Implement a stub-API
  - Use Actions and unit test
 
--------------------------------------------------------------------------------------------------------------------------------

Phase 2:
--------------------------------------------------------------------------------------------------------------------------------

- Use Flask as your WEB service platform
  - Reference 1:  https://palletsprojects.com/p/flask/ (Github:  https://github.com/pallets/flask )
  - Reference 2:  Flask-RESTFUL  (Github:  https://github.com/flask-restful/flask-restful )
- Step 2:  Integrate your module to become a RESTFUL system
  - Deploy your system to free AWS services:  https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc
  - Develop simple WEB applications to test your system.
  - Document your REST APIs on your Github
 
--------------------------------------------------------------------------------------------------------------------------------

Phase 3:
--------------------------------------------------------------------------------------------------------------------------------

- Focus on Ingestor module
- Investigate PDF to Text conversions
  - How to Extract Data from PDF Forms Using Python
  - pdfreader
  - Python for Pdf
  - PDFMiner
  - Fork of PDFMiner
  - Pdfplumber
- Chose module you want to use and implement uploader and Ingester
- For storage, use a folder.  No need for cloud storage.
- For extracted text, store the data in files.  No database yet.  This will be phase 3. (?)
- Due Date 2/28/2021.  It is strict this time because we want to use the database concept and implement other modules.

- First Deliverable:  Due Date: **3/1/2021**
  - Setup mysql or MongoDB
  - Create your database (Tables in case of mysql or containers in case of MongoDB)
  - Define your data storage strategy
- Second Deliverable:  Due Date: **3/7/2021**
  - Extract Text from PDF files
  - Store Data in Database
  - Dates this time are strict because we want to use the database concept and implement other modules.


--------------------------------------------------------------------------------------------------------------------------------
