#!/usr/bin/env python
import urllib2, string, smtplib
from email.mime.text import MIMEText
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
