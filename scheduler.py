#!/usr/bin/env python
# coding: utf-8

import tweepy, time, sys
import keys as k

argfile = str(sys.argv[1])

API_KEY = k.apiKey
API_SECRET = k.apiSecret
CONSUMER_TOKEN = k.accessToken
CONSUMER_SECRET = k.accessSecret

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(CONSUMER_TOKEN, CONSUMER_SECRET)
api = tweepy.API(auth)

filename = open(argfile,'r')
f = filename.readlines()
filename.close()

for line in f:
    api.update_status(line)
    print('tweet number', f.index(line)+1, 'posted')
    sys.stdout.flush()
    time.sleep(5)