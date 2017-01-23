import json
import tweepy

import tweet_secrets as secrets


auth = tweepy.OAuthHandler(secrets.KEY, secrets.SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
