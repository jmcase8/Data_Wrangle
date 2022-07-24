# Data Wrangling

#### Video Demo: <URL HERE>

-----

## Purpose
The project started off as a way to learn more about module creation/testing/implementation, utilize a version contorl system (VCS; I used git), utilize python virtual environment (venv) for packaging and requirements, use I/O effectively, and handle various exceptions. Overall, the utility of the module began to grow and now it can be used by anyone desiring a quick and efficient way to gather data and assess data. 

## Files

### project.py
The goal of this module is to gather data for local storage, and perform a basic completeness and consistency check on the data. The module is meant to expedite time spent gathering data
by doing most of the leg work for you, and, in addition it will help point you to errors in the data.

This module accepts either a local path or url at the CLI, and takes either a file or zip compressed folder. If the url is a file, the file will be downloaded and subsequently processed. 
If the url led to a zip folder, it will be downloaded and unzipped. If a path is entered, the file will be processed. If the path is a zip it will be unzipped. 

Currently only supports .zip compressed files. Data files supported are: '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods','.odt', '.txt', '.data', '.csv', '.dat', '.tsv'

### test_project.py
This file implements various tests on the functionality of project.py. It can be ignored if you only want to use the module. The links used in test_project.py are linked in a later section.

### test_files and test.zip
Folder of test files and a test zip to run pytests. If not desired they do not need to be downloaded. The data is from the (UCI Machine Learning Repository)[https://archive.ics.uci.edu/ml/index.php]. Specifically the (Iris dataset)[https://archive.ics.uci.edu/ml/datasets/Iris] and the (Dry Bean dataset)[https://archive.ics.uci.edu/ml/datasets/Dry+Bean+Dataset].

### requirements.txt
Text file detailing required packages.

### pytest.ini
Initialization file for using the test_project.py to avoid depreciation warnings. Can be ignored if you do not plan on testing.