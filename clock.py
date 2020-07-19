import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyrebase


def setup_db():
    config = {
    "apiKey": "AIzaSyAiHMVgcJ7H1TN9ulWt_njXG4oS-CgZEHo",
        "authDomain": "leor-jewish-service.firebaseapp.com",
        "databaseURL": "https://leor-jewish-service.firebaseio.com/",
        "storageBucket": "leor-jewish-service.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("unibidinc@gmail.com", "password")
    db = firebase.database()
    return(db)

def send_text_tmobile(message,number, subject):
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
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email,sms_gateway,sms)
    server.quit()

def timesNewYork(keys):
    d = datetime.datetime.today()
    today = d.strftime('%m/%d/%Y')
    jewish_times = requests.get("https://wyrezmanim.herokuapp.com/api/zmanim?timezone=America/New_York&latitude=40.7128&longitude=-74.0060&date=%s&elevation=33&format=json" % (today))
    message = ''
    message += 'New York\n'
    message += 'Date: ' + today + '\n' + '\n'
    for key in keys:
        message += key + ': ' + jewish_times.json()[key] + '\n'
    return(message)

def timesJerusalem(keys):
    d = datetime.datetime.today()
    today = d.strftime('%m/%d/%Y')
    jewish_times = requests.get("https://wyrezmanim.herokuapp.com/api/zmanim?timezone=Asia/Jerusalem&latitude=31.7683&longitude=35.2137&date=%s&elevation=800&format=json" % (today))
    message = ''
    message += 'Jerusalem\n'
    message += 'Date: ' + today + '\n' + '\n'
    for key in keys:
        message += key + ': ' + jewish_times.json()[key] + '\n'
    return(message)


sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='sun-fri', hour=6)
def scheduled_job():
    keys = ['SolarMidnight', 'Alos', 'Sunrise', 'SofZmanShmaGra',
            'SofZmanTefilahGra', 'Chatzos','MinchaGedolah', 'MinchaKetana',
            'PlagHamincha','Shkia','BainHashmashosRabeinuTam2Stars', 'Tzais']
    NY_message = timesNewYork(keys)
    send_text_tmobile(NY_message, '+15166039008', 'New York')
    print('Messages sent successfully')



sched.start()


