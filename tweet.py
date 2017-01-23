# -*- coding: utf-8 -*-

import json
import tweepy
import re
import tweet_secrets as secrets

from user_prompts import *


class Tweet(object):

    # twitter api uses OAuth for authorisation so set it up below
    auth = tweepy.OAuthHandler(secrets.key, secrets.SECRET)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

    api = tweepy.API(auth)  # initialize a tweepy API class with credentials

    def __init__(self):
        self.userName = None
        self.period = None
        self.terminate = None

    def prompt(self):
        try:
            self.userName = input(user_prompts.user_name)
            # check if user used @ and remove it
            if re.match(r'^@', self.userName):
                chars = self.userName.split()
                chars.remove('@')
                self.userName = ''.join(chars)
            user_data = tweepy.Cursor(api.user_timeline,
                                      id=self.userName).item(1)
        except TweepError as t:
            print(t['message'])
            print(user_prompts.invalid_user)
