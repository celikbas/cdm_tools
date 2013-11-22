#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "Zeki Celikbas"
__copyright__   = "Copyright 2013, cdm_tools Project"
__license__     = "GPL"
__version__     = "0.0.1"
__email__       = "celikbas@itu.edu.tr"
__status__      = "Experiment"

import csv
import os
import glob

reader = csv.reader(open('31_Ekim13CDM.txt', 'rb'), delimiter='\t')

# creat log files
dir_log = open('dir_log.txt','w')
error_log = open('error_log.txt','w')
fixed_csv = open('fixed.csv','wb')

# Find the location of coloumn includes the pdf file names.
header = reader.next()
filename = header.index("FileName")

#write header line to the fixed csv file as first line.
headerLine = '\t'.join(map(str, header))
fixed_csv.write(headerLine + '\r\n')

for row in reader:
    #find out the pdf file from csv record.
    DIR = row[filename]
    PDF = DIR + '.pdf'

    # check if the pdf file exist in folder:
    if os.path.exists(PDF):
        # if this file proceesed befor the directory must be created. Empty it!
        if os.path.exists(DIR):
            files = glob.glob(DIR+'/*')
            for f in files:
                os.remove(f)

            message = "DIRECTORY EXIST. Old files removed: " + DIR + '\n'
            dir_log.write(message)
        else:
            # if not create the folder with the pdf name:
            os.mkdir(DIR)
            message = 'Folder created ' + DIR + '\n'
            dir_log.write(message)
            # print message

        # now time to proceed pdf file:
        COMMD = 'pdfimages -j ' + PDF + ' ' + DIR + '/' + DIR
        os.system(COMMD)
        message = "File processed to folder: " + DIR + '\n'
        dir_log.write(message)

        # Creatin a new csv file with the corresponding csv record+folder.
        headerLine = '\t'.join(map(str, row))
        fixed_csv.write(headerLine + '\r\n')
        
        files = glob.glob(DIR+'/*')
        for f in files:
            dir_log.write(' ' + f + '\n')
        print message
    else:
        message = "ERROR: File not exist: " + PDF + '\n'
        dir_log.write(message)
        error_log.write(message)
        #print message

dir_log.close()
error_log.close()
fixed_csv.close()

print "All logs written to dir_log.txt file"
print "Error logs also written to error_log.txt file"
