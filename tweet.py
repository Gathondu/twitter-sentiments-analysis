# -*- coding: utf-8 -*-

import json
import tweepy
import os
import sys
import re
import tweet_secrets as secrets
import user_prompts

import tweet_tables as Tables
from colorclass import Color
from tqdm import tqdm
from sentiments import getSentiment
from time import sleep


class Tweet():

    def __init__(self):
        # twitter api uses OAuth for authorisation so set it up below
        self.auth = tweepy.OAuthHandler(secrets.KEY, secrets.SECRET)
        self.auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_SECRET)

        # initialize a tweepy API class with credentials
        self.api = tweepy.API(self.auth)
        self.userName = None
        self.tweets = None
        self.userTweets = {}
        self.jsonFile = 'tweets.json'
        self.wordCount = {}
        self.validName = False
        self.rt = True

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _exit(self):
        quit = input("Are you sure you want to quit? [y]/n ")
        if quit.lower() not in ('n', 'no'):
            self._clear()
            # hack to validate username before displaying it
            if self.validName:
                sys.exit(user_prompts.exit.format('@', self.userName))
            sys.exit(user_prompts.exit.format('!', '!'))
            os.remove('tweets.json')
        else:
            self._clear()
            self.view()

    # Function that checks if a file exists
    def exist(self, file):
        if os.path.exists(file):
            # if the file exists open it and clear everything inside
            f = open(file, 'w')
            f.close()

    def is_valid(self, name):
        try:
            if name.lower() in ('q', 'quit'):
                self.validName = False
                return False
            user = self.api.get_user(screen_name=name)
            self.validName = True
            return True
        except tweepy.TweepError:
            self.validName = True
            return False

    def validateUser(self, name):
        print("Validating user.....")
        # check if user want's to quit
        if name.lower() in ('q', 'quit'):
            self._exit()
        if not self.is_valid(name):
            print(user_prompts.invalid_user)
            self.prompt()
            self.validateUser(self.userName)

    # function to validate number of tweets to fetch is valid
    def validateTweetNumber(self, number):
        # check if user want's to quit
        if number.lower() in ('q', 'quit'):
            self._exit()

        # check input is an integer
        while not re.match(r'\d', number):
            number = input(user_prompts.invalid_tweets)
            self._clear()

        while int(number) < 1 or int(number) > 10:
            number = input(user_prompts.invalid_tweets)
            self._clear()
        return int(number)

    def prompt(self):
        self.userName = input(user_prompts.user_name)

        # check if to quit
        if self.userName in ('q', 'quit'):
            self._exit()

        # check if user used @ and remove it
        if re.match(r'^@', self.userName):
            chars = list(self.userName)
            chars.remove('@')
            self.userName = ''.join(chars)

        # if the propmt is called from within instance skip
        if self.tweets is None:
            self.tweets = input(user_prompts.tweets)
            rt = input(user_prompts.rt)
            if rt.lower() in ('n', 'no'):
                self.rt = False
            else:
                self.rt = True
            self._clear()
            self.tweets = self.validateTweetNumber(self.tweets)
        else:
            result = input(user_prompts.change_tweets).lower()
            self._clear()
            if result not in ('n', 'no'):
                self.tweets = input(user_prompts.tweets)
                rt = input(user_prompts.rt)
                if rt.lower() in ('n', 'no'):
                    self.rt = False
                else:
                    self.rt = True
                self._clear()
                self.tweets = self.validateTweetNumber(self.tweets)

    def getTweets(self, user, rt):
        text = "Fetching tweets @{}. Please wait".format(user)
        with tqdm(
             total=self.tweets, unit='B', unit_scale=True, desc=text) as pbar:
            for twit in self.fetchTweets(user, rt):
                details = {}
                details['date'] = str(twit.created_at)
                details['tweet'] = twit.text
                details['sentiments'] = getSentiment(twit.text)
                self.userTweets[twit.id] = details
                pbar.update(1)
            pbar.close()

    def fetchTweets(self, user, rt):
        # get user tweets
        return tweepy.Cursor(
            self.api.user_timeline, id=user,
            include_rts=rt).items(self.tweets)

    def dumpJson(self, file):
        f = open(file, 'w')
        json.dump(self.userTweets, f, indent=4)
        f.close()

    def viewPage(self):
        result = input(user_prompts.views)
        # check if to quit
        if result in ('q', 'quit'):
            self._exit()
        # check for numbers
        while not re.match(r'\d', result):
            self._clear()
            print(Color('{red}@{}, please enter a number in the list!{/red}')
                  .format(self.userName))
            self.view()

        # check number in listed items
        while int(result) not in list(range(1, 5)):
            self._clear()
            print(Color('{red}@{}, please enter a number in the list!{/red}')
                  .format(self.userName))
            self.view()

        return int(result)

    def view(self):
        page = self.viewPage()
        # 1. Help
        if page == 1:
            self._clear()
            print(user_prompts.help.format(self.userName))
            h = input('\n\n PRESS ENTER KEY TO GO BACK')
            self._clear()
            self.view()

        # 2. View Tweets
        if page == 2:
            try:
                self._clear()
                print(Tables.viewTweets(self.userName, self.tweets))
                more = input(user_prompts.more_tweets.format(self.tweets))
                while int(more) in list(range(1, self.tweets+1)):
                    self._clear()
                    print(Tables.viewTweets(self.userName, more))
                    h = input('\n\n PRESS ENTER KEY TO GO BACK')
                    self._clear()
                    self.view()
                else:
                    self._clear()
                    self.view()
            except ValueError:
                self._clear()
                self.view()

        # 3. View words ranks
        if page == 3:
            self._clear()
            print(Tables.viewRanks(self.tweets))
            h = input('\n\n PRESS ENTER KEY TO GO BACK')
            self._clear()
            self.view()

        # 4. View sentiments analysis
        if page == 4:
            self._clear()
            print(Tables.viewSentiments(self.tweets))
            h = input('\n\n PRESS ENTER KEY TO GO BACK')
            self._clear()
            self.view()
