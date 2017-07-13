import json
import re
import requests
import sendgrid
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from sendgrid.helpers.mail import *

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
sched = BlockingScheduler()
sg = sendgrid.SendGridAPIClient(apikey=cfg['SENDGRID_APIKEY'])
FROM_EMAIL = Email("OpenTableScheduler@example.com")
TO_EMAIL = Email(cfg['EMAIL'])
SUBJECT = "Open Table Scheduler"


@sched.scheduled_job('interval', minutes=5)
def timed_job():
    request_url = "https://www.opentable.com/restaurant/profile/{}/search".format(
        cfg['OPENTABLE_ID']
    )
    payload = {
        'covers': cfg['PEOPLE'],
        'dateTime': cfg['DATETIME']
    }

    resp = requests.post(request_url, payload)
    data = json.loads(resp.text)

    # Because the stupid fucking response has availability in an HTML string -_-'
    availability = data['availability'].encode('utf')
    dates_times = re.findall('data-datetime=".*?"', availability)
    dates = []
    for d in dates_times:
        date = d.partition('"')[-1].rpartition('"')[0]
        date = datetime.strptime(date, '%Y-%m-%d %H:%M')

        date_start = datetime.strptime(cfg['DATE_SEARCH_START'], '%Y-%m-%d')
        date_end = datetime.strptime(cfg['DATE_SEARCH_END'], '%Y-%m-%d')

        if date > date_start and date < date_end:
            time_start = cfg['TIME_SEARCH_START']
            if time_start:
                time_start = datetime.strptime(time_start, '%H:%M').time()

            time_end = cfg['TIME_SEARCH_END']
            if time_end:
                time_end = datetime.strptime(time_end, '%H:%M').time()

            if date.time() > time_start and date.time() < time_end:
                dates.append(date)

    message = ""
    if len(dates) > 0:
        for d in dates:
            message += d.strftime("%a %b %d %Y %I:%M %p") + "<br>"

    if message != "":
        message = "AVAILABILITY:<br>" + message
        content = Content("text/html", message)
        mail = Mail(FROM_EMAIL, SUBJECT, TO_EMAIL, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print("EMAIL SENT")
        print(response.status_code)


message = "Starting Availability Check for OpenTable Restaurant {} for {} to {}".format(
    cfg['OPENTABLE_ID'],
    cfg['DATE_SEARCH_START'],
    cfg['DATE_SEARCH_END']
)
content = Content("text/html", message)
mail = Mail(FROM_EMAIL, SUBJECT, TO_EMAIL, content)
response = sg.client.mail.send.post(request_body=mail.get())
print("INIT EMAIL SENT")
sched.start()
