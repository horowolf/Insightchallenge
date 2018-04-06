# README


#Programming language

Python 3.6.1

#Addition library used

Non

#Running environments

OS: Mac OS High Sierra

IDE: PyCharm CE, with interpreter: Anaconda

#The way to solve this challenge

Main problems:

1 Super huge input data from SEC is the final objective.

    -> Need to handle the inputs when reading it.
    
    -> Check inactivity session every second(the input's timestamp).
    
2 The order of output based on "the order of the sessions become inactive" > "the order of the sessions came in".

    -> Need to record the input timestamp but also won't make the record become too big.
    
Check how the idea of solution can be implement:

1 Use hash table -> use dictionary

2 Compare the timestamps -> use datetime

Start coding: Put the place holder as comment in code for reminding the design. (look the code in src/uncleaned.py)

#How to run

Basically, run run.sh in Terminal should be fine.

If the shell isn't works, than enter the command with format:

python success.py input-log.csv input-inactivity_period.txt output-file.txt

#Reference

docs.python.org

https://stackoverflow.com/questions/17262256/how-to-read-one-single-line-of-csv-data-in-python

https://stackoverflow.com/questions/431752/python-csv-reader-how-do-i-return-to-the-top-of-the-file/431771

#Copyrights

Source code in src: Yu-Ting Chen

Test case in "your-own-test_1": Modified files from Insight Data Engineering Team

Others: Insight Data Engineering Team
