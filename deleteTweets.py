#!/usr/bin/env python
# coding: utf-8
# https://pythonmarketer.com/2020/09/13/delete-all-your-tweets-with-tweepy-and-the-twitter-api/

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
    print("You are about to delete all tweets from the account @%s." % api.verify_credentials().screen_name)
    print("Does this sound ok? Type yes to carry out this action.")
    do_delete = input("> ")
    if do_delete.lower() == 'y' or do_delete.lower() == 'yes':
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(status.id)
                print("Deleted:", status.id)
            except Exception:
                traceback.print_exc()
                print("Failed to delete:", status.id)
 
if __name__ == "__main__":
    # api = oauth_login(ACCESS_TOKEN, ACCESS_SECRET)
    # print("Authenticated as: %s" % api.me().screen_name)
     
    batch_delete(api)