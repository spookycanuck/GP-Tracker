# How to use:
#   1. to run this code from a heroku server:
#       - use Heroku keys
#       - use command "heroku run worker" in terminal
#   2. to run this code from local, use local key variables
#       - use Local keys
#       - use command "py scheduler.py" in terminal

# Heroku Keys
# API_KEY = environ['CONSUMER_KEY']
# API_SECRET = environ['CONSUMER_SECRET']
# ACCESS_TOKEN = environ['ACCESS_TOKEN']
# ACCESS_SECRET = environ['ACCESS_SECRET']

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

def reminder_tweeter():
    i = 0
    sleepTime = 1

    for line in race_list:
        try:
            if (race_list[i]['time'] != 'Race Completed'):
                if race_list[i]['time'] != 'Race has been CANCELED':
                    now = datetime.now()
                    race = race_list[i]['time']
                    raceTimeObj = parser.parse(race)
                    current_time = now.replace(microsecond=0)
                    time_diff = raceTimeObj - current_time
                    td_sec = time_diff.total_seconds()
                    td_hr = td_sec/(60 * 60)
                    if (race_list[i]['watch'] != 'No info available'):
                        if(24 < td_hr <= 96):
                            api.update_status("\nIt's race week!!\nThe " + race_list[i]['race'] + " is this weekend!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST] on " + race_list[i]['time'][:6])
                            print('96hrs - tweet', i+1, 'posted')  
                            logging.info('REMINDER:: 96hrs - tweet ' + str(i+1) + ' posted')                     
                        elif(12 < td_hr <= 24):
                            api.update_status("\nRACE DAY!\n The " + race_list[i]['race'] + " is less than 24hrs away!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST]")
                            print('24hrs - tweet', i+1, 'posted')
                            logging.info('REMINDER:: 24hrs - tweet ' + str(i+1) + ' posted')
                        elif (1 < td_hr <= 12):
                            api.update_status("\nREMINDER!\n The " + race_list[i]['race'] + " is less than 12hrs away!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST]")
                            print('12hrs - tweet', i+1, 'posted')
                            logging.info('REMINDER:: 12hrs - tweet ' + str(i+1) + ' posted')
                        elif (0 < td_hr <= 1):
                            api.update_status("\nIt's almost time!\n The " + race_list[i]['race'] + " is less than an hour away!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST]")
                            print('1hr! - tweet', i+1, 'posted')
                            logging.info('REMINDER:: 1hr! - tweet ' + str(i+1) + ' posted')
                        elif (-1 <= td_hr <= 0):
                            api.update_status("\nLIGHTS OUT!\n The " + race_list[i]['race'] + " is underway!\n Watch on  " +
                                race_list[i]['watch'])
                            print('lights out! - tweet', i+1, 'posted')
                            logging.info('REMINDER:: lights out! - tweet ' + str(i+1) + ' posted')
                        elif(td_hr > 169):
                            pass
                        elif(96 < td_hr):
                            print('\nGreater than 96 hours until', race_list[i]['race'], '- no tweet posted')
                            print(round(td_hr, 2), 'hrs left\n')
                            logging.info('REMINDER::Greater than 96 hours until ' + race_list[i]['race'] + ' (' + str(round(td_hr, 2)) + 'hrs) - no tweet posted')
                        elif(td_hr < -1):
                            print('\n---', race_list[i]['race'],'completed! ---')
                            pass
                        else:
                            print('\n--- No condition matching for', race_list[i]['race'],'---')
                    else:
                        print("no watch info")
            sys.stdout.flush()
            i += 1
        except Exception as e:
            print("*****\nException Error:\n*****")
            print(e)
            pass

# scheduler = BlockingScheduler()
# scheduler.add_job(reminder_tweeter, 'interval', hours=12, start_date='2022-05-20 09:00:00', end_date='2022-05-23 10:05:00')
# scheduler.add_job(next_race, 'interval', days=7, start_date='2022-05-22 13:00:00', end_date='2022-05-23 10:00:00')
# print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

reminder_tweeter() # Posts reminders the week leading up to race day, based on time until race, to Twitter
