#!/usr/bin/env python
# coding: utf-8
# https://pythonmarketer.com/2020/09/13/delete-all-your-tweets-with-tweepy-and-the-twitter-api/

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
    print("You are about to delete tweets from the account @%s." % api.verify_credentials().screen_name)
    print("Does this sound ok? Type yes to carry out this action.")
    do_delete = input(">> ")
    if do_delete.lower() == 'y' or do_delete.lower() == 'yes':
        for status in tweepy.Cursor(api.user_timeline).items():
            x.append(status)
        if (len(x)<50):
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    api.destroy_status(status.id)
                    print("Deleted:", status.id)
                    sys.stdout.flush()
                except Exception:
                    traceback.print_exc()
                    print("Failed to delete:", status.id)
                    sys.stdout.flush()
        else:
            print("\nERROR: More than 50 tweets detected!\nHow many would you like to delete?")
            delete_num = input(">> ")
            print("\nYou are about to delete", delete_num, "tweets from the account @%s." % api.verify_credentials().screen_name)
            print("Does this sound ok? Type yes to carry out this action.")
            delete_res = input(">> ")
            if int(delete_num) >= 1:
                if delete_res.lower() == 'y' or delete_res.lower() == 'yes':
                    for status in x[-int(delete_num):]:
                        try:
                            api.destroy_status(status.id)
                            print("Deleted:", status.id)
                            sys.stdout.flush()
                        except Exception:
                            traceback.print_exc()
                            print("Failed to delete:", status.id)
                            sys.stdout.flush()
 
if __name__ == "__main__":
    # api = oauth_login(ACCESS_TOKEN, ACCESS_SECRET)
    # print("Authenticated as: %s" % api.me().screen_name)
     
    batch_delete(api)