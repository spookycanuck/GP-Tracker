from datetime import datetime, date
from dateutil import parser
import csv

FILENAME = 'files/scheduleX.csv'
INDEX = 0

headers = []
race_list = []
output_X = []

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


# Matches date string
# =========================
# today = date.today()
# current_date = today.strftime("%b-%d-%Y")

# print("Date: ", current_date.replace('-',' ').replace('0','')[:6])
# print("Race: ", race_list[4]['date'][:6])

# dateClean = current_date.replace('-',' ').replace('0','')[:6]
# raceClean = race_list[4]['date'][:6]

# if (dateClean.strip() == raceClean.strip()):
#     print("Match!")
# else:
#     print("no match :(")


def normalizeTime():
# ========================
# Matches time string
# ========================
    now = datetime.now()
    race = race_list[INDEX]['time']
    print("\nRace time from CSV: ", race)
    print("Current time:", now)

    # raceTimeObj = datetime.strptime(race_list[4]['time'],'%b %d - %I:%M %p')
    raceTimeObj = parser.parse(race)
    current_time = now.replace(microsecond=0)

    print('\n-----------------')
    print("Race time as local dt Obj: ", raceTimeObj)
    print("Current time as clean dt Obj: ", current_time)

    time_diff = raceTimeObj - current_time
    td_sec = time_diff.total_seconds()
    td_hr = td_sec/(60 * 60)
    print('\n-----------------')
    print('time diff: ', time_diff)
    print('total hrs: ', round(td_hr, 2), '\n')

def makeNewList():
    now = datetime.now()
    for i, x in enumerate(race_list):
        # print(x['time'])
        if (x['time'] == "Race Completed"):
            print(x['time'])
        elif (x['time'] == "Race has been CANCELED"):
            print(x['time'])
        else:
            raceTimeX = parser.parse(x['time'])
            # print(raceTimeX)
            current = now.replace(microsecond=0)
            time_d = raceTimeX - current
            td_sec = time_d.total_seconds()
            td_hr = td_sec/(60 * 60)
            if (td_hr < 0):
                print('Race Completed_X')
            else:
                print(x['date'])
                race_X = {
                    "date": x['date'],
                    "race": x['race'],
                    "location": x['location'],
                    "time": x['time'],
                    "watch": x['watch']
                }
                output_X.append(race_X)
                with open('files/scheduleX.csv', 'w') as csvfile: 
                    wr = csv.DictWriter(csvfile, fieldnames=headers) 
                    wr.writeheader()
                    wr.writerows(output_X)

normalizeTime()
# makeNewList()