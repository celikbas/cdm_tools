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
dir_log = open('dir_log.txt','w')
error_log = open('error_log.txt','w')
fixed_csv = open('fixed.csv','wb')

# Find the location of the column that includes the pdf file names.
header = reader.next()
filename = header.index("FileName")

#write header line to the fixed csv file as the first line.
headerLine = '\t'.join(map(str, header))
fixed_csv.write(headerLine + '\r\n')

for row in reader:
    #find out the pdf file from csv record.
    PDF = row[filename]
    if '.pdf' in PDF:
        DIR = os.path.splitext(PDF)[0]
    else:
        DIR1 = PDF
        DIR = PDF + "/scans"
        PDF = PDF + '.pdf'

    # check if the pdf file exists in the folder:
    if os.path.exists(PDF):
        # if this file was processed before, the directory must be 
        # emptied!
        if os.path.exists(DIR):
            files = glob.glob(DIR+'/*')
            for f in files:
                os.remove(f)

            message = "DIRECTORY EXISTS. Old files removed: " + DIR + '\n'
            dir_log.write(message)
        else:
            # Create the folder with the pdf's name:
            os.mkdir(DIR1)
            os.mkdir(DIR1+"/scans")
            message = 'Folder created ' + DIR1 + '\n'
            dir_log.write(message)
            # print message

        # now time to proceed to the pdf file:
        # COMMD = 'pdfimages -j ' + PDF + ' ' + DIR + '/'
        # convert -density $DENSITY -quality $QUALITY $FILE $NEWDIR/
        # scans/page_%03d.jpg
        density = 200
        quality = 85
        files = glob.glob('*.pdf')
        print "The PDF file %s is being split into several pages and \
watermark image is being added..."%(DIR1+".pdf")
        for f in files:
            CMD = "convert -density %s -quality %s  %s %s/page_%s.jpg"\
%(density, quality, f, DIR,"%03d")
            # print CMD
            os.system(CMD)
            files2 = glob.glob(DIR+"/*")
            # Adding watermark to all images processed from the PDF
            #file.
            for f2 in files2:
                CMD2 = "composite -dissolve 10 -gravity southeast \
itulogo_grey226.png %s %s"%(f2, f2)
                os.system(CMD2)
                
        message = "Files were processed in the folder: " + DIR + '\n'
        dir_log.write(message)
        
        # Creating a new csv file with the corresponding csv
        # record+folder.
        headerLine = '\t'.join(map(str, row))
        fixed_csv.write(headerLine + '\r\n')
        
        files = glob.glob(DIR+'/*')
        for f in files:
            dir_log.write(' ' + f + '\n')
        print message
    else:
        message = "ERROR: File does not exist: " + PDF + '\n'
        dir_log.write(message)
        error_log.write(message)
        #print message

dir_log.close()
error_log.close()
fixed_csv.close()

print "All logs written to dir_log.txt file"
print "Error logs also written to error_log.txt file"
