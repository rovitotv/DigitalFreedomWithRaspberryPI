#!/bin/python
#
# test sends a SpamTest email message that will definitely be marked
# as spam.  There is a neat trigger called GTUBE (generic trigger for
# unsolicited bulk Email)
#
# WARNING: Be sure to set the you adress and the ip address to your inside
# Raspberry Pi.  In addition you have to add your Raspberry Pi Address to
# the variable for inside networks TODO check this variable name.
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

import smtplib

from email.mime.text import MIMEText

sendStr = "this is a test email that will trigger spam\n"
sendStr += "XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X"
msg = MIMEText(sendStr)
msg['Subject'] = 'Spam trigger for sure'
# me == the sender's email address
# you == the recipient's email address
me = 'spamking@randomdomain.com'
you = 'rovitotv@rovitotv.org'
msg['From'] = you
msg['To'] = me

s = smtplib.SMTP('192.168.1.9')
s.sendmail(me, [you], msg.as_string())
s.quit()
