#!/usr/bin/env python
# coding: utf-8

import tweepy, time, sys
import keys as k

API_KEY = k.apiKey
API_SECRET = k.apiSecret
ACCESS_TOKEN = k.accessToken
ACCESS_SECRET = k.accessSecret

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def batch_delete(api):
    print("Get all tweets from the account @%s?" % api.verify_credentials().screen_name)
    print("Type yes to carry out this action.")
    do_delete = input("> ")
    if do_delete.lower() == 'y' or do_delete.lower() == 'yes':
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.get_status(status.id)
                print("Tweet ID:", status.id)
            except Exception:
                traceback.print_exc()
                print("Failed to retrieve ID:", status.id)
 
if __name__ == "__main__":
    # api = oauth_login(ACCESS_TOKEN, ACCESS_SECRET)
    # print("Authenticated as: %s" % api.me().screen_name)
     
    batch_delete(api)