# Determines the next race on the schedule. Posts update to Twitter.

from os import environ
from datetime import datetime, date
from dateutil import parser
import tweepy, time, sys, csv
import logging, logging.handlers, os
import keys as k

# Set up event logging
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "./files/logs/scheduler.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
root.addHandler(handler)

# Local Keys
API_KEY = k.apiKey
API_SECRET = k.apiSecret
ACCESS_TOKEN = k.accessToken
ACCESS_SECRET = k.accessSecret

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

headers = []
race_list = []

FILENAME = 'files/scheduleX.csv'

with open(FILENAME, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            headers = row
        else:
            if (row):
                race = {
                    headers[0]: row[0],
                    headers[1]: row[1],
                    headers[2]: row[2],
                    headers[3]: row[3],
                    headers[4]: row[4],
                }
                race_list.append(race)

def next_race():
    now = datetime.now()
    futureRace = []
    nextRace = []
    # print(now)

    i = 0
    y = 0
    for x in race_list:
        if race_list[i]['time'][:6] == 'Race C' or race_list[i]['time'][:6] == 'CANCEL' or race_list[i]['time'] == 'Race has been CANCELED':
            # print("canceled " + str(i))
            pass
        else:
            dateCalc = race_list[i]['time']
            # print(dateCalc)
            dateObj = parser.parse(dateCalc)
            if now <= dateObj:
                futureRace.append(str(dateObj))
                if y == 0:
                    nextRace.append(race_list[i])
                    y += 1
                else:
                    pass
            else:
                pass
        i += 1
    
    try:
        api.update_status("The next race is the " + nextRace[0]['race'] + ".\nRace time is scheduled for " + nextRace[0]['time'][-8:] + " EST on " +
            nextRace[0]['time'][:6] + ".\nCheck back here for schedule & reminder updates!")
        print("next race tweet posted")
        logging.info("NEXT_RACE:: next race tweet posted")
    except Exception as e:
        print("\n*****\nException Error:\n*****")
        print(e)
        pass

# next_race()
