import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_text(message):
    email = "unibidinc@gmail.com"
    pas = "lera apiq jhgi wuko"
    sms_gateway = '+15166039008@tmomail.net'
    smtp = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp,port)
    server.starttls()
    server.login(email,pas)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    msg['Subject'] = "JEWISH ZMANIM!!!!"
    body = message
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email,sms_gateway,sms)
    server.quit()

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=3)
def scheduled_job():
    d = datetime.datetime.today()
    today = d.strftime('%m/%d/%Y')
    jewish_times = requests.get("https://wyrezmanim.herokuapp.com/api/zmanim?timezone=America/New_York&latitude=40&longitude=-73&date=%s&elevation=50&format=json" % (today))
    message = ''
    for key, value in jewish_times.json().items():
        message += key + ': ' + value + '\n'
    send_text(message)

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    d = datetime.datetime.today()
    today = d.strftime('%m/%d/%Y')
    jewish_times = requests.get("https://wyrezmanim.herokuapp.com/api/zmanim?timezone=America/New_York&latitude=40&longitude=-73&date=%s&elevation=50&format=json" % (today))
    message = ''
    for key, value in jewish_times.json().items():
        message += key + ': ' + value + '\n'
    send_text(message)
sched.start()


