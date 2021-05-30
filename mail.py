from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

MY_ADDRESS = os.environ['MY_ADDRESS']
PASSWORD = os.environ["PASSWORD"]

def sendEmail(email, title, contents):
    s = smtplib.SMTP(host='c4c.org.pl', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    msg = MIMEMultipart()
    message = contents
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']=title
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    del msg