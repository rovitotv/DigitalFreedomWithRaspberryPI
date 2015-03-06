#!/bin/python
# This script attempts automatic install of web server and its
# needed dependencies.  It assumes you are running this with
# sudo command or as root.  Testing environment is Debian Wheezy.
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


if __name__ == "__main__":
	data = {}
	getHostIPAddress(data)
	installApache()
	testApache(data)
	installPHP()
	testPHP(data)
	print("webserver automatic install complete")
