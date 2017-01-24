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
        self.statuses = None
        self.terminate = None
        self.user = None

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def validateUser(self, name):
        user = self.api.get_user(screen_name=name)
        if user.screen_name is None:
            return False
        return True

    def prompt(self):
        self.userName = input(user_prompts.user_name)
        self._clear()
        # check if user used @ and remove it
        if re.match(r'^@', self.userName):
            chars = list(self.userName)
            chars.remove('@')
            self.userName = ''.join(chars)

        # validate the user name
        if not self.validateUser(self.userName):
            print(user_prompts.invalid_user)
            self.prompt()  # NOT RUNNING????

        # welcome user
        print(user_prompts.welcome.format(self.userName))

        self.statuses = input(user_prompts.statuses)
        self._clear()
        while self.statuses < 0 and self.statuses > 500:
            self.statuses = input(user_prompts.invalid_statuses)
            self._clear()

        self.user = tweepy.Cursor(api.user_timeline,
                                  id=self.userName).items(self.statuses)
        

t = Tweet()
t.prompt()
