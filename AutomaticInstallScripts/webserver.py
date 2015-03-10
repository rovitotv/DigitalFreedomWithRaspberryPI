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
import argparse

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
	output = sp.check_output("apt-get install php5 libapache2-mod-php5 -y", 
		shell=True)
	print("%s" % output)

def testPHP(data):
	output = sp.check_output("mv /var/www/index.html /var/www/index.old", 
		shell=True)
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

def installMySQL(data):
	print("Installing MySQL")
	com = "export DEBIAN_FRONTEND=noninteractive && apt-get install mysql-server php5-mysql -y"
	output = sp.check_output(com, shell=True)
	print("%s" % output)
	# now setup the password
	com = "mysqladmin -u root password %s" % (data['passwordMySQL'])
	output = sp.check_output(com, shell=True)
	print("%s" % output)

def installWordPress(data):
	print("Installing WordPress")
	com = "cd /var/www && chown www-data: . && rm -f index.php && "
	com += "wget http://wordpress.org/latest.tar.gz && "
	com += "tar xzf latest.tar.gz && "
	com += "mv wordpress/* . && "
	com += "rm -rf wordpress latest.tar.gz"
	output = sp.check_output(com, shell=True)
	print("%s" % output)
	print("createing WordPress database")
	com = ('mysql -uroot -p%s -e "create database wordpress;"' 
		% data['passwordMySQL'])
	output = sp.check_output(com, shell=True)
	print("%s" % output)

def waitForWordPressInstallToComplete(data):
	urlOfRaspberryPi = "http://" + data['ipAddressString']
	message = "Now you must use a web browser to configure WordPress.  Using \n"
	message += "a web browser on the same network as your Raspberry Pi, go \n"
	message += "to the followig url: %s \n" % (urlOfRaspberryPi)
	message += "Now follow the instructions in the guide filling out the \n"
	message += "correct database information.  \n"
	print(message)

	while 1 == 1:
		wordPressComplete = raw_input('Is the WordPress configuration completed? (y/n): ')
		if wordPressComplete == 'y' or wordPressComplete == 'Y':
			break

	message = "It's recommended that you change your permalink settings to \n"
	message += "make your URLs more friendly. To do this, log in to WordPress \n"
	message += "and go to the dashboard. Go to Settings then Permalinks. \n"
	message += "Select the Post name option and click Save Changes. After \n"
	message += "saving, you will be prompted to update your .htaccess file \n"
	message += "which this script will do automatcially as soon as you press \n"
	message += "yes."
	print(message)

	while 1 == 1:
		wordPressComplete = raw_input('Are the permalink settings set? (y/n): ')
		if wordPressComplete == 'y' or wordPressComplete == 'Y':
			break

def installHtAccessFile(data):
	f = open('/var/www/.htaccess', 'w')
	f.write("<IfModule mod_rewrite.c>\n")
	f.write("RewriteEngine On\n")
	f.write("RewriteBase /\n")
	f.write("RewriteRule ^index\.php$ - [L]\n")
	f.write("RewriteCond %{REQUEST_FILENAME} !-f\n")
	f.write("RewriteCond %{REQUEST_FILENAME} !-d\n")
	f.write("RewriteRule . /index.php [L]\n")
	f.write("</IfModule>\n")
	f.close()
	com = "sudo a2enmod rewrite"
	output = sp.check_output(com, shell=True)
	print("%s" % output)

def modifyApacheDefaltConfigurationFile(data):
	'''
		Changes the apache default configuration file.
	'''
	f = open("/etc/apache2/sites-available/default", "r")
	lines = f.read()
	splitLines = lines.split("\n")
	splitLines[10] = "                AllowOverride All"
	f.close()
	f = open("/etc/apache2/sites-available/default", "w")
	for i in range(0, len(splitLines)):
		f.write(splitLines[i] + '\n')
	f.close()

def restartApache(data):
	print("restarting apache")
	com = "service apache2 restart"
	output = sp.check_output(com, shell=True)
	print("%s" % output)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--passwordMySQL", help="MySQL password",
		action="store", required=True)
	args = parser.parse_args()
	data = {}
	data['args'] = args
	data['passwordMySQL'] = args.passwordMySQL
	getHostIPAddress(data)
	installApache()
	testApache(data)
	installPHP()
	testPHP(data)
	installMySQL(data)
	installWordPress(data)
	waitForWordPressInstallToComplete(data)
	installHtAccessFile(data)
	modifyApacheDefaltConfigurationFile(data)
	restartApache(data)
	print("webserver automatic install complete")
