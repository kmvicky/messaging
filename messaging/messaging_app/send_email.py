import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from messaging.messaging_app.models import *

def send_email(email_data):

	comment = email_data.get('comment')
	sender = email_data.get('sender')
	send_to = email_data.get('send_to')

	sender_email = email_data.get('sender_email')
	receiver_email = email_data.get('receiver_email')
	password = 'random'

	message = MIMEMultipart("alternative")
	message["Subject"] = "multipart test"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Create the plain-text and HTML version of your message
	text = """\
	Hi {},
	{} has commented on conversation {} '{}' """.format(send_to, sender, comment.conversation.description, comment.comment)

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(text, "plain")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(sender_email, password)
			server.sendmail(
					sender_email, receiver_email, message.as_string()
			)