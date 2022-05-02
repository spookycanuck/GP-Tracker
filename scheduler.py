#!/usr/bin/env python
# coding: utf-8

import tweepy, time, sys
# import keys as k
from os import environ

argfile = str(sys.argv[1])

# Import keys from Heroku 
API_KEY = environ['CONSUMER_KEY']
API_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']

# API_KEY = k.apiKey
# API_SECRET = k.apiSecret
# ACCESS_TOKEN = k.accessToken
# ACCESS_SECRET = k.accessSecret

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

filename = open(argfile,'r')
f = filename.readlines()
filename.close()

for line in f:
    api.update_status(line)
    print('tweet number', f.index(line)+1, 'posted')
    sys.stdout.flush()
    time.sleep(15)