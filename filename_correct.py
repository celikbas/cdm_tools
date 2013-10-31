#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" wfnr.py: Word File Name Replace """

__author__ 	= "Zeki Celikbas" 
__copyright__ 	= "Copyright 2013, The X Project" 
__license__ 	= "GPL" 
__version__ 	= "0.0.1" 
__email__ 	= "celikbas@itu.edu.tr" 
__status__ 	= "Experiment"


# define our method
def replace_all(text, dic):
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text

# characters and replacements
reps = {'ç':'c', 'Ç':'C', 'ı':'i', 'İ':'I', 'ğ':'g', 'Ğ':'G', 'ö':'o', 'Ö':'O', 'ü':'u', 'Ü':'U', 'ş':'s', 'Ş':'S', ' ':'_'}

import os
import re

pattern = re.compile('ç|Ç|ı|İ|ğ|Ğ|ö|Ö|ü|Ü|ş|Ş| ')

count = 0
files = filter(os.path.isfile, os.listdir('.'))
for file in files:
	if pattern.findall(file):
	    print 'Rename: ' , file , ' => ', replace_all(file, reps)
	    os.rename(file, replace_all(file, reps))
	    count +=1
	    
print count , ' file name changed'

"""
# folders and files:
for file in os.listdir('.'):
	if pattern.findall(file):
		print file
"""		
