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
        self.tweets = None
        self.terminate = None
        self.userTweets = None
        self.jsonFile = 'tweets.json'
        self.wordCount = {}

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Function that checks if a file exists
    def exist(self, file):
        if os.path.exists(file):
            # if the file exists open it and clear everything inside
            f = open(file, 'w')
            f.close()

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

        self.tweets = input(user_prompts.tweets)
        self._clear()

        # check input is an integer
        while not re.match(r'\d', self.tweets):
            self.tweets = input(user_prompts.invalid_tweets)
            self._clear()

        while int(self.tweets) < 1 or int(self.tweets) > 500:
            self.tweets = input(user_prompts.invalid_tweets)
            self._clear()

        # get user tweets
        self.userTweets = tweepy.Cursor(self.api.user_timeline,
                                        id=self.userName).items(
                                        int(self.tweets))

        # check if file exsist. create if doesn't and clean if exsists
        self.exist(self.jsonFile)

        f = open(self.jsonFile, 'w')
        # dump data to file
        for twit in self.userTweets:
            json.dump(twit.text, f, skipkeys=True,
                      ensure_ascii=False)
        f.close()
t = Tweet()
t.prompt()
