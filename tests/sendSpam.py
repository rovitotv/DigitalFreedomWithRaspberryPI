#!/bin/python
# this test sends a SpamTest email message that will definitely be marked
# as spam.  There is a neat trigger called GTUBE (generic trigger for
# unsolicited bulk Email)
import smptlib

from email.mime.text import MIMEText

msg = "this is a test email that will trigger spam\n"
msg += "XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X"
msg['Subject'] = 'Spam trigger for sure'
me = 'rovitotv@rovitotv.org'
you = 'spamking@randomdomain.com'
msg['From'] = you
msg['To'] = me

s = smtplib.SMTP('192.168.1.26')
s.sendmail(me, [you], msg.as_string())
s.quit()