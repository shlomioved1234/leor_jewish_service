import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_text(message,number):
    email = "unibidinc@gmail.com"
    pas = "lera apiq jhgi wuko"
    sms_gateway = '%s@tmomail.net' % number
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
    message += jewish_times.json()['SolarMidnight']
    message += jewish_times.json()['Alos']
    message += jewish_times.json()['Sunrise']
    message += jewish_times.json()['SofZmanTefilahGra']
    message += jewish_times.json()['SofZmanShemaMGA']
    message += jewish_times.json()['SofZmanShemaGra']
    message += jewish_times.json()['SofZmanShema3HoursBeforeChatzos']
    message += jewish_times.json()['Chatzos']
    message += jewish_times.json()['MinchaGedolah']
    message += jewish_times.json()['Mincha Ketana']
    message += jewish_times.json()['Shkia']
    message += jewish_times.json()['BainHashmashosRabeinuTam2Stars']
    message += jewish_times.json()['Tzais']
    message += jewish_times.json()['Candle Lighting']
    send_text(message, '+15166039008')

@sched.scheduled_job('interval', seconds = 5)
def timed_job():
    print("I'm alive")


sched.start()


