# -*- coding: utf-8 -*-

import json
import tweepy
import re
import tweet_secrets as secrets
import user_prompts


class Tweet(object):

    def __init__(self):
        # twitter api uses OAuth for authorisation so set it up below
        self.auth = tweepy.OAuthHandler(secrets.KEY, secrets.SECRET)
        self.auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

        # initialize a tweepy API class with credentials
        self.api = tweepy.API(self.auth)
        self.userName = None
        self.period = None
        self.terminate = None

    def prompt(self, user=None):
        try:
            self.userName = user or input(user_prompts.user_name)
            # check if user used @ and remove it
            if re.match(r'^@', self.userName):
                chars = list(self.userName)
                chars.remove('@')
                self.userName = ''.join(chars)
            user_data = tweepy.Cursor(self.api.user_timeline,
                                      id=self.userName).items(1)
        except tweepy.error.TweepError as t:
            print(t['message'])
            print(user_prompts.invalid_user)

t = Tweet()
t.prompt('@456dfg')
