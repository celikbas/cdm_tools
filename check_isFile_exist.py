#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "Zeki Celikbas"
__copyright__   = "Copyright 2013, cdm_tools Project"
__license__     = "GPL"
__version__     = "0.0.2"
__email__       = "celikbas@itu.edu.tr"
__status__      = "Working"

import csv
import os
import glob
import sys
from time import time
zaman_baslangic = time()
if len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
        CSVFILE = sys.argv[1]
    else:
        print "csv file does not exist! Please specify a file."
        sys.exit()
else:
    print "no csv file was provided. Please specify a file."
    sys.exit()
        
reader = csv.reader(open(CSVFILE, 'rb'), delimiter='\t')

# create log files
isFile_exist = open('isFile_exist.txt','w')

# Find the location of the column that includes the pdf file names.
header = reader.next()
filename = header.index("FileName")

#write header line to the fixed csv file as the first line.
headerLine = '\t'.join(["FileName", "Found"])
isFile_exist.write(headerLine + '\r\n')

count_Found = 0
count_NotFound = 0
for row in reader:
    #find out the pdf file from csv record.
    PDF = row[filename]
    PDF = PDF.strip()
    PDF = PDF + '.pdf'

    # check if the pdf file exists in the folder:
    if os.path.exists(PDF):
        message = '\t'.join([PDF, "Found"])
        count_Found += 1
    else:
        # Create the folder with the pdf's name:
        message = '\t'.join([PDF, "NOT Found"])
        count_NotFound += 1

    isFile_exist.write(message + '\r\n')

isFile_exist.close()

print "*"*80
print "All logs written to isFile_exist.txt file"
print "TOTAL LINES examined: ", count_Found + count_NotFound
print "Found Files: ", count_Found 
print "Not Found Files: ", count_NotFound
print "*"*80
