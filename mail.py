from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import threading
from datetime import datetime, timedelta

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

def everyHour(Plant, email):
    def send():
        threading.Timer(3600.0, send).start()
        current = datetime.now()
        onehago = current-timedelta(hours = 1)
        update = "Hello!! Nice to see you again!! Check out these new plants:\n"
        plants = Plant.query.filter(Plant.DateTime >= onehago).\
            filter(Plant.DateTime <= current)
        for plant in plants:
            pl_data = {'lat': plant.Latitude, 'lng': plant.Longitude, 'name': plant.PlantType,'health': plant.Health}
            update+="-Type: "+pl_data["name"]+"; Health:"+pl_data["health"]+"; Location:"+str(pl_data["lat"])+", "+str(pl_data["lng"])+"\n"
        sendEmail(email, "Hourly update!", update)
        print("Message sent!!", email, update)
    send()