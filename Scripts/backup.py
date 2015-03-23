#!/bin/python
# This script performs a automatic backup.  A user must provide specific
# arguments.
#
#
# Copyright (c) 2015, Todd V. Rovito All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import datetime
import os
import subprocess as sp

def getCurrentDate(data):
	i = datetime.datetime.now()
	data['year'] = i.year
	data['month'] = i.month
	data['day'] = i.day

def makeBackupDirectory(data):
	data['backupDirectory'] += "/%04d%02d%02dRaspberryPiBack" % (data['year'],
		data['month'], data['day'])
	if os.path.exists(data['backupDirectory']):
		fileList = os.listdir(data['backupDirectory'])
		for f in fileList:
			os.remove(data['backupDirectory'] + "/" + f)
	else:
		os.mkdir(data['backupDirectory'])

def backupWordPressDatabase(data):
	backupFileName = data['backupDirectory'] + "/WordPress.bak.sql.bz2"
	com = ("mysqldump --add-drop-table -h localhost -u root -p%s wordpress" %
		data['passwordMySQL'])
	com += " | bzip2 -c > %s" % backupFileName
	output = sp.check_output(com, shell=True)
	print output

def backupWordPressContent(data):
	backupFileName = data['backupDirectory'] + "/WordPressContentUploads.zip"
	com = "cd /var/www/wp-content/uploads/ && zip -r %s *" % backupFileName
	output = sp.check_output(com, shell=True)
	print output

def backupLargeMediaFiles(data):
	if not os.path.exists('/var/www/LargeMediaFiles'):
		return

	backupFileName = data['backupDirectory'] + "/LargeMediaFiles.zip"
	com = "cd /var/www/LargeMediaFiles/ && zip -r %s *" % backupFileName
	output = sp.check_output(com, shell=True)
	print output

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-b", "--backupDirectory", help="path to backup dir",
		action="store", required=True)
	parser.add_argument("-p", "--passwordMySQL", help="MySQL password",
		action="store", required=True)
	args = parser.parse_args()
	data = {}
	data['args'] = args
	data['backupDirectory'] = args.backupDirectory
	data['passwordMySQL'] = args.passwordMySQL
	getCurrentDate(data)
	makeBackupDirectory(data)
	backupWordPressDatabase(data)
	backupWordPressContent(data)
	backupLargeMediaFiles(data)
