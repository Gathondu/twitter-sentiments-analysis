# -*- coding: utf-8 -*-

import pprint
import json
import tweepy
import csv

import tweet_secrets as secrets


auth = tweepy.OAuthHandler(secrets.KEY, secrets.SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

api = tweepy.API(auth)
user_tweets = tweepy.Cursor(api.user_timeline, screen_name="Nimzee_Nimo").items(1)
# tweets_json = json.loads(user_tweets)

for tweet in user_tweets:
    pprint.pprint(tweet._json['user']['screen_name'], indent=1)

# print('Name: ' + user_name)
# print('Location: ' + user_location)
# print('Friends: ' + str(user_friends_count))

public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.user_name)

