#!/bin/python
# This script attempts automatic install of web server and its
# needed dependencies.  It assumes you are running this with
# sudo command or as root.  Testing environment is Debian Wheezy.
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

import subprocess as sp
import httplib
import sys

def getHostIPAddress(data):
	output = sp.check_output("hostname -I", shell=True)
	output = output[0:-2]
	data['ipAddressString'] = output
	
def installApache():
	print("Installing apache2")
	output = sp.check_output("apt-get install apache2 -y", shell=True)
	print("%s" % output)

def testApache(data):
	output = sp.check_output("service apache2 start", shell=True)
	print("%s" % output)
	conn = httplib.HTTPConnection(data['ipAddressString'])
	conn.request("GET", "/index.html")
	r1 = conn.getresponse()
	if r1.reason != "OK":
		print("apache2 failed to produce OK response when reading index.html\n")
		sys.exit(5)
	readData = r1.read()
	dataLines = readData.split("\n")
	if dataLines[0] != "<html><body><h1>It works!</h1>":
		print("index.html page does not start correctly\n")
		sys.exit(5)
	else:
		print("Apache2 installed and tested")

def installPHP():
	print("Installing php")
	output = sp.check_output("apt-get install php5 libapache2-mod-php5 -y", shell=True)
	print("%s" % output)

def testPHP(data):
	output = sp.check_output("mv /var/www/index.html /var/www/index.old", shell=True)
	print("%s" % output)
	output = sp.check_output("echo \"<?php echo date('Y-m-d H:i:s');\" > /var/www/index.php",
		shell=True)
	print("%s" % output)
	conn = httplib.HTTPConnection(data['ipAddressString'])
	conn.request("GET", "/index.php")
	r1 = conn.getresponse()
	if r1.reason != "OK":
		print("apache2 failed to produce OK response when reading index.php\n")
		sys.exit(5)
	readData = r1.read()
	print readData

	print("PHP installed and tested")

def installMySQL():
	print("Installing MySQL")
	com = "export DEBIAN_FRONTEND=noninteractive && apt-get install mysql-server php5-mysql -y"
	output = sp.check_output(com, shell=True)
	print("%s" % output)


if __name__ == "__main__":
	data = {}
	getHostIPAddress(data)
	installApache()
	testApache(data)
	installPHP()
	testPHP(data)
	installMySQL()
	print("webserver automatic install complete")
