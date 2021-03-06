#!/usr/bin/env python

import re
import argparse
import time
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

#You're email credentials
gmail_user = "youremail@gmail.com"
gmail_pwd = "yourpassword"

email_address 	= ""
attachment  	= ""
email_text 		= ""
email_subject	= ""


#This function receives all the user input and checks to see if the input provided is valid
def user_input():
	global email_address, attachment, email_text, email_subject
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--destination', help='destination of the email', dest='to', type=str, required=True)
	parser.add_argument('-t','--title', help='Title of the message', dest='title', type=str, required=True)
	parser.add_argument('-m','--message', help='The message you want to send', dest='text', type=str, required=True)
	parser.add_argument('-f', '--file', help='file to attach', dest='file', type=str, required=True)
	args = parser.parse_args()
	
	email_address 	= args.to
	attachment 	  	= args.file
	email_text		= args.text
	email_subject	= args.title


	#Check to see if the destination email address is valid
	pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
	email_validity = bool(re.match(pattern, email_address))
	if email_validity != True:
		print "Enter a valid email address"
		time.sleep(2)
		exit(1)
	else:
		if not os.path.isfile(attachment):
			print "%s is not a valid filename, enter a valid file name"%attachment
			time.sleep(2)
			exit(1)
		
		
	#In the final last step of checking that all the input requirements have been met
	#We make sure that the message of the email is not an empty string
	if not len(email_text) or not len(email_subject):
		print "Message and title/subject string should not be empty"
		time.sleep(2)
		exit(1)
		
		
		
#This function is the where the all the mail processing is done
def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()
   
   
if __name__ == '__main__':
	user_input()
	mail(email_address, email_subject, email_text, attachment)
   
   
