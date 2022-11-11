# Posts entire F1 schedule from CSV to Twitter

from os import environ
from datetime import datetime, date
from dateutil import parser
import tweepy, time, sys, csv
import logging, logging.handlers, os
import keys as k

# Set up event logging
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "files/logs/scheduler.log"))
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

# print(race_list)

def schedule_tweeter():
    i = 0
    sleepTime = 1

    for line in race_list:
        if (race_list[i]['time'] != 'Race Completed'):
            if race_list[i]['time'] != 'CANCELED':
                if (race_list[i]['watch'] != 'No info available'):
                        api.update_status("\nThe " + race_list[i]['race'] + " will be held on " + race_list[i]['time']
                                + " [EST] - at The " + race_list[i]['location'] +
                                "\n\nIt can be viewed on " + race_list[i]['watch'])
                        print('tweet', i+1, 'posted')
                        time.sleep(sleepTime)
                else:
                    api.update_status("\nThe " + race_list[i]['race'] + " will be held on " + race_list[i]['time']
                            + " [EST] - at The " + race_list[i]['location'] +
                            "\n\nNo watch info available")
                    print('tweet', i+1, 'posted - no watch info')
                    time.sleep(sleepTime)
            else:
                api.update_status("\nThe " + race_list[i]['race'] + " originally scheduled for " + race_list[i]['date'][:3] + ' ' + race_list[i]['date'][-2:]
                        + " has been " + race_list[i]['time'])
                print('tweet', i+1, 'posted - canceled')
                time.sleep(sleepTime)
        else:
            print('race completed - no tweet posted')
            time.sleep(1)
        sys.stdout.flush()
        i += 1

schedule_tweeter() 
