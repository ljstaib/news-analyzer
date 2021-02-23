# Homework #2 for EC500 at BU: news-analyzer-ljstaib

Copyright @2021 
Luke Staib 
ljstaib@bu.edu

Status: Phase 2 in progress, Phase 3 completed 
--------------------------------------------------------------------------------------------------------------------------------

Phase 1: Completed
- Stub-API modules for Phase 1 are in their respective .py files. I also have psuedocode in newsanalyzer_pseudocode.txt.
Phase 2: In progress
- Working on integrating my modules to be a RESTFUL system
Phase 3: Completed
- Please see NLP_analysis.py for the ConvertFilesToText() function. I can currently convert from TXT and PDF files.

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

--------------------------------------------------------------------------------------------------------------------------------
