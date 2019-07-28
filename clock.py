import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def send_text(message):
    resp = requests.post('https://textbelt.com/text', {
                         'phone': '5166039008',
                         'message': message,
                         'key': 'textbelt',
                         })

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

sched.start()


