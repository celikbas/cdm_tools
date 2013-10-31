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

reader = csv.DictReader(open('31_Ekim13CDM.csv', 'rb'), delimiter='\t')

for row in reader:
	DIR = row.get('FileName')
	PDF = DIR + '.pdf'
	if not os.path.exists(DIR):
		os.mkdir(DIR)
		print "Folder created: " + DIR

	if os.path.exists(PDF):
		COMMD = 'pdfimages -j ' + PDF + ' ' + DIR + '/' + DIR
		os.system(COMMD)
		print "File processed to folder " + DIR + " Command: " + COMMD


