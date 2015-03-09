#!/bin/python
# This script removes all the packages and puts the system back to original
# state.  It assumes you are running this with
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

def putOldIndexFilesBack():
	output = sp.check_output("rm /var/www/index.php", shell=True)
	print("%s" % output)
	output = sp.check_output("mv /var/www/index.old /var/www/index.html", shell=True)
	print("%s" % output)

def uninstallPackages():
	output = sp.check_output("sudo apt-get remove mysql-server php5-mysql -y",
		shell=True)
	print(output)
	output = sp.check_output("sudo apt-get remove apache2 php5 libapache2-mod-php5 -y",
		shell=True)
	print(output)

def stopServices():
	output = sp.check_output("sudo service apache2 stop", shell=True)
	print("%s" % output)
	output = sp.check_output("sudo service mysql stop", shell=True)
	print("%s" % output)

if __name__ == "__main__":
	putOldIndexFilesBack()
	uninstallPackages()
	stopServices()
	print("webserver automatic un-install complete")