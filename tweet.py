import json
import tweepy
import csv

import tweet_secrets as secrets


auth = tweepy.OAuthHandler(secrets.KEY, secrets.SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

api = tweepy.API(auth)
user = api.me()

print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))

public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.user_name)

