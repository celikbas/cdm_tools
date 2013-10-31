#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" move_jpg-fold.py: Move Jpeg files to their correct Folders """

__author__ 	= "Zeki Celikbas" 
__copyright__ 	= "Copyright 2013, cdm_tools Project" 
__license__ 	= "GPL" 
__version__ 	= "0.0.1" 
__email__ 	= "celikbas@itu.edu.tr" 
__status__ 	= "Experiment"

import os
import re

files = os.listdir('.')

images = [img for img in files if img.endswith('.jpg')]

images.sort()

for image in images:
	img = image[:-4]
	print re.sub("_\d{1,2}$", "", img)

