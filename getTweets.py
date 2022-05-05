#!/usr/bin/env python
# coding: utf-8

import tweepy, time, sys
import keys as k

# Import keys from keys.py
API_KEY = k.apiKey
API_SECRET = k.apiSecret
ACCESS_TOKEN = k.accessToken
ACCESS_SECRET = k.accessSecret

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def batch_delete(api):
    x=[]
    print("Get tweets from the account @%s?" % api.verify_credentials().screen_name)
    print("Type yes to carry out this action.")
    get_tweets = input(">> ")
    if get_tweets.lower() == 'y' or get_tweets.lower() == 'yes':
        for status in tweepy.Cursor(api.user_timeline).items():
            x.append(status)
        if (len(x)<50):
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    api.get_status(status.id)
                    print("Tweet ID:", status.id)
                    sys.stdout.flush()
                except Exception:
                    traceback.print_exc()
                    print("Failed to retrieve ID:", status.id)
                    sys.stdout.flush()
        else:
            print("\nERROR: More than 50 tweets detected!\nPrinting the last 15:")
            for status in x[-15:]:
                try:
                    api.get_status(status.id)
                    print("Tweet ID:", status.id)
                    sys.stdout.flush()
                except Exception:
                    traceback.print_exc()
                    print("Failed to retrieve ID:", status.id)
                    sys.stdout.flush()

 
if __name__ == "__main__":
    # api = oauth_login(ACCESS_TOKEN, ACCESS_SECRET)
    # print("Authenticated as: %s" % api.me().screen_name)
     
    batch_delete(api)