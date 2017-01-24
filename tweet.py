# -*- coding: utf-8 -*-

import json
import tweepy
import os
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

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def prompt(self):
        try:
            self.userName = user or input(user_prompts.user_name)
            self._clear()
            # check if user used @ and remove it
            if re.match(r'^@', self.userName):
                chars = list(self.userName)
                chars.remove('@')
                self.userName = ''.join(chars)

            # welcome user
            print(user_prompts.welcome.format(self.userName))

            self.period = input(user_prompts.period)
            self._clear()
            while self.period not in str(list(range(1, 9))):
                self.period = input(user_prompts.invalid_period)
            print(self.period)
        except Exception as e:
            print(e.args[0])
            print(user_prompts.invalid_user)
