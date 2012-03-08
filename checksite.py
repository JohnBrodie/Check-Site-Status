#!/usr/bin/env python
# This prgram is Licenced under GPL, see http://www.gnu.org/copyleft/gpl.html
# Author: John Brodie
# Search for specific message in webpage, send email if we don't find it,
# or if we get an HTTP error code.
import ConfigParser
import urllib2
import smtplib
import socket

from email.mime.text import MIMEText
from os.path import expanduser


def check_site():
    """ Make request, catch any errors and send a mail."""
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config_file = expanduser('~/.checksite.cfg')
    config.read(config_file)
    try:
        site = config.get('Required', 'site')
        mail_server = config.get('Required', 'mail_server')
        mail_port = config.get('Required', 'mail_port')
        fromaddr = config.get('Required', 'from_addr')
        toaddr = config.get('Required', 'to_addr')
        password = config.get('Required', 'password')
        check = config.get('Required', 'check')
        timeout = config.getint('Required', 'timeout')

    except ConfigParser.NoOptionError, error:
        print error
        return 4

    socket.setdefaulttimeout(timeout)

    mailserv = smtplib.SMTP(mail_server, mail_port)

    # Default error:
    err = '(No error code found)'
    body = ''

    try:
        resp = urllib2.urlopen(site)
        body = resp.read()

    except urllib2.HTTPError as error:
        err = str(error.code)

    except urllib2.URLError, error:
        err = str(error.reason)

    if check not in body:
        text = 'Could not find text "%s" at %s.  Error: %s' \
                % (check, site, err)
        msg = MIMEText(text)
        msg['Subject'] = "Automated site failure notification"
        msg['From'] = fromaddr
        msg['To'] = toaddr
        mailserv.ehlo('x')
        mailserv.starttls()
        mailserv.ehlo('x')
        mailserv.login(fromaddr, password)
        mailserv.sendmail(fromaddr, toaddr, msg.as_string())
        mailserv.quit()

if __name__ == '__main__':
    check_site()
