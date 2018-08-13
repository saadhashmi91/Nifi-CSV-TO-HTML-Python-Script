#!/usr/bin/env python
# csv2html
# Copyright (c) 2013, 2014, 2017 dbohdan. All rights reserved.
# License: BSD (3-clause). See the file LICENSE.
'''
This module converts CSV files to HTML tables. It can be used as a standalone
program.
'''
from __future__ import print_function
from . import __version__
from . import tablegen
import os
import sys
import csv
import java.io
from StringIO import StringIO
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback


DEFAULT_DELIMITER = ','
PYTHON2 = sys.version_info[0] == 2 
 
class ModJSON(StreamCallback):


	def __init__(self):
		pass
	def process(self, inputStream, outputStream):
    
		text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
	#Read the CSV stream.
	
		delim = ','
		nstart = 0
		skipheader = False
		renum = False
		title=''
		completedoc = False
		attrs={'table': 'border=1'}
		file_like_io = StringIO(text)
		csv_reader = csv.reader(file_like_io, dialect='excel', delimiter=delim)
		nrow = 0  # The row number counter.
		
		if PYTHON2:
			def next_row():
				return csv_reader.next()
		else:
			def next_row():
				return csv_reader.__next__()
				
		outputStream.write(tablegen.start(completedoc, title, attrs))
		
		if not skipheader:
			row = next_row()
			outputStream.write(tablegen.row(row, True, attrs))
			nrow += 1
		while nrow < nstart:
			next_row()
			nrow += 1
		for row in csv_reader:
			if renum:
				# If there is no zeroth header row, add 1 to the new row number
				# to correct for the rows being counted from zero. Do the same if
				# we're counting from nstart.
				row[0] = str(nrow - nstart + int(skipheader or nstart > 0))
			outputStream.write(tablegen.row(row, False, attrs))
			nrow += 1
		outputStream.write(tablegen.end(completedoc))
		
		
		
		#obj = json.loads(text)
		#newObj = {
		#      "Source": "NiFi",
		#      "ID": obj['id'],
		#      "Name": obj['user']['screen_name']
		#    }
		'''outputStream.write(bytearray(json.dumps(newObj, indent=4).encode('utf-8')))'''
 
flowFile = session.get()
if (flowFile != None):
  flowFile = session.write(flowFile, ModJSON())
  flowFile = session.putAttribute(flowFile, "filename", flowFile.getAttribute('filename').split('.')[0]+'_translated.html')
session.transfer(flowFile, REL_SUCCESS)
session.commit()