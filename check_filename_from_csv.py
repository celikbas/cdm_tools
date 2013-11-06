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

reader = csv.DictReader(open('31_Ekim13CDM.txt', 'rb'), delimiter='\t')

dir_log = open('dir_log.txt','w')
error_log = open('error_log.txt','w')
for row in reader:
    DIR = row.get('FileName')
    PDF = DIR + '.pdf'

    if os.path.exists(PDF):
        if os.path.exists(DIR):
            files = glob.glob(DIR+'/*')
            for f in files:
                os.remove(f)

            message = "DIRECTORY EXIST. Old files removed: " + DIR + '\n'
            dir_log.write(message)
        else:
            os.mkdir(DIR)
            message = 'Folder created ' + DIR + '\n'
            dir_log.write(message)
            # print message
    
        COMMD = 'pdfimages -j ' + PDF + ' ' + DIR + '/' + DIR
        os.system(COMMD)
        message = "File processed to folder: " + DIR + '\n'
        dir_log.write(message)
        files = glob.glob(DIR+'/*')
        for f in files:
            dir_log.write(' ' + f + '\n')
        # print message
    else:
        message = "ERROR: File not exist: " + PDF + '\n'
        dir_log.write(message)
        error_log.write(message)
        #print message

dir_log.close()
error_log.close()

print "All logs written to dir_log.txt file"
print "Error logs also written to error_log.txt file"

