checksite.py is a simple python script that checks for a specified message on a website, and emails someone if it is not found, along with any error code encountered along the way.

The message checking allows you to make sure that your site is not just UP, but functioning properly.  Especially useful for sites running web frameworks that will not return an HTTP error code if they are misconfigured.

Installation
============

Copy `checksite.py` to $HOME/bin, make appropriate permissions.

    mkdir -p $HOME/bin
    cp checksite.py $HOME/bin
    chmod +x $HOME/bin/checksite.py

Open checksite.py with your favorite editor, and fill your details in the username/password/mailserv/site/message fields.
Note that this file now contains your email server password, and so should be duly restricted.  `man chmod` for more info.

Run with `python checksite.py`.  To make it more useful, put it in your crontab:

- Make sure you have access to crontab.
- Use `crontab -e` to open your crontab for editing.
- Add a line to run checksite as often as desired.  For example:
`*/15 * * * * /home/ogmios/bin/checksite`
...will run the script every 15 minutes.
- Note cron does not like spaces in file names, so:
`mv $HOME/bin/checksite.py $HOME/bin/checksite`

Requirements
============

- python >= 2.5

Author: John Brodie <jdb356@drexel.edu>
