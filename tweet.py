# -*- coding: utf-8 -*-

import json
import tweepy
import tweet_secrets as secrets


class Tweet(object):

    # twitter api uses OAuth for authorisation so set it up below
    auth = tweepy.OAuthHandler(secrets.key, secrets.SECRET)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

    api = tweepy.API(auth)  # initialize a tweepy API class with credentials
