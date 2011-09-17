#!/usr/bin/env python
# This prgram is Licenced under GPL, see http://www.gnu.org/copyleft/gpl.html
# Author: John Brodie
# Search for specific message in webpage, send email if we don't find it, or if we get an HTTP error code.
import urllib2, string, smtplib, socket
from email.mime.text import MIMEText

timeout = 10 #Timeout in seconds
socket.setdefaulttimeout(timeout)
site="http://example.com" #Site we want to check on.
message="blah blah blah" #Message we are verifying against.
mailserv= smtplib.SMTP("smtp.gmail.com", 587) #Server,port
fromaddr="you@example.com"
toaddr="someonestressed@example.com"
password="example"

err = '(No error code found)' #Placeholder for error message, if there is one.
body = ''
try:
	f = urllib2.urlopen(site)
	body = f.read()
except urllib2.HTTPError as e:
	err=str(e.code)
except urllib2.URLError, e:
	err=str(e.reason)

if string.find(body,message) == -1:
	msg = MIMEText("Could not find text \" "+message+"\" at "+site+"\n Recieved error: " +err)
	msg['Subject'] = "Automated site failure notification"
	msg['From'] = fromaddr
	msg['To'] = toaddr
	mailserv.ehlo('x')
	mailserv.starttls()
	mailserv.ehlo('x')
	mailserv.login(fromaddr, password)
	mailserv.sendmail(fromaddr,toaddr,msg.as_string())
	mailserv.quit()
