# How to use:
#   1. to run this code from a heroku server:
#       - use Heroku keys
#       - use command "heroku run worker" in terminal
#   2. to run this code from local, use local key variables
#       - use Local keys
#       - use command "py scheduler.py" in terminal

from os import environ
from datetime import datetime, date
from dateutil import parser
import tweepy, time, sys, csv
import keys as k

# Heroku Keys
# API_KEY = environ['CONSUMER_KEY']
# API_SECRET = environ['CONSUMER_SECRET']
# ACCESS_TOKEN = environ['ACCESS_TOKEN']
# ACCESS_SECRET = environ['ACCESS_SECRET']

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

with open('files/schedule4.csv', mode='r') as csv_file:
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

def reminder_tweeter():
    i = 0
    sleepTime = 1

    for line in race_list[:6]:
        try:
            if (race_list[i]['time'] != 'Race Completed'):
                if race_list[i]['time'] != 'CANCELED':
                    now = datetime.now()
                    race = race_list[i]['time']
                    raceTimeObj = parser.parse(race)
                    current_time = now.replace(microsecond=0)
                    time_diff = raceTimeObj - current_time
                    td_sec = time_diff.total_seconds()
                    td_hr = td_sec/(60 * 60)
                    if (race_list[i]['watch'] != 'No info available'):
                        if(24 < td_hr < 96):
                            api.update_status("\nIt's race week!!\nThe " + race_list[i]['race'] + " is this weekend!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST] on" + race_list[i]['time'][:6])
                            print('96hrs - tweet', i+1, 'posted')                       
                        elif(12 < td_hr < 24):
                            api.update_status("\nRACE DAY!\n The " + race_list[i]['race'] + " is less than 24hrs away!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST]")
                            print('24hrs - tweet', i+1, 'posted')
                        elif (1 < td_hr < 12):
                            api.update_status("\nREMINDER!\n The " + race_list[i]['race'] + " is less than 12hrs away!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST]")
                            print('12hrs - tweet', i+1, 'posted')
                        elif (0 < td_hr <= 1):
                            api.update_status("\nIt's almost time!\n The " + race_list[i]['race'] + " is less than an hour away!\n Watch on  " +
                                race_list[i]['watch'] + " at " + race_list[i]['time'][-8:] + " [EST]")
                            print('1hr! - tweet', i+1, 'posted')
                        elif (-1 < td_hr <= 0):
                            api.update_status("\nLIGHTS OUT!\n The " + race_list[i]['race'] + " is underway!\n Watch on  " +
                                race_list[i]['watch'])
                            print('lights out! - tweet', i+1, 'posted')
                        elif(96 < td_hr):
                            print('\nGreater than 96 hours until', race_list[i]['race'], '- no tweet posted')
                            print(i)
                            print(td_hr)
                            print(line, '\n')
                        else:
                            print('\n--- No condition matching for', race_list[i]['race'],'---')
            sys.stdout.flush()
            i += 1
        except Exception as e:
            print("*****\nException Error:\n*****")
            print(e)
            pass


def next_race():
    now = datetime.now()
    futureRace = []
    nextRace = []
    # print(now)

    i = 0
    y = 0
    for x in race_list:
        if race_list[i]['time'][:6] == 'Race C' or race_list[i]['time'][:6] == 'CANCEL':
            pass
        else:
            dateCalc = race_list[i]['time']
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
    except Exception as e:
        print("\n*****\nException Error:\n*****")
        print(e)
        pass

# schedule_tweeter() # Posts entire F1 schedule from CSV to Twitter
reminder_tweeter() # Posts reminders the week leading up to race day, based on time until race, to Twitter
# next_race() # Determines the next race on the schedule. Posts update to Twitter.