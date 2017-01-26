# -*- coding: utf-8 -*-

import json
import tweepy
import os
import sys
import re
import tqdm
import tweet_secrets as secrets
import user_prompts
from colorclass import Color

from tables import *


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
        self.validName = False

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
        else:
            self._clear()
            self.prompt()

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
        # check if user want's to quit
        if name.lower() in ('q', 'quit'):
            self._exit()
        if not self.is_valid(name):
            print(user_prompts.invalid_user)
            self.prompt()
            self.validateUser(self.userName)

    # functioin to validate number of tweets to fetch is valid
    def validateTweetNumber(self, number):
        # check if user want's to quit
        if number.lower() in ('q', 'quit'):
            self._exit()

        # check input is an integer
        while not re.match(r'\d', number):
            number = input(user_prompts.invalid_tweets)
            self._clear()

        while int(number) < 1 or int(number) > 500:
            number = input(user_prompts.invalid_tweets)
            self._clear()
        return number

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
            self._clear()
            self.tweets = self.validateTweetNumber(self.tweets)
        else:
            result = input(user_prompts.change_tweets).lower()
            self._clear()
            if result not in ('n', 'no'):
                self.tweets = input(user_prompts.tweets)
                self._clear()
                self.tweets = self.validateTweetNumber(self.tweets)

    def getTweets(self, user, number):
        # get user tweets
        self.userTweets = tweepy.Cursor(self.api.user_timeline,
                                        id=user).items(
                                        int(number))

    def dumpJson(self, tweets, file):
        # dump data to file
        count = 1
        tweetDict = {}
        detailsDict = {}  # stores the details of the tweet like time created
        for tweet in tweets:
            key = "tweet " + str(count)
            # convert datetime to string to make it json serializable
            detailsDict['date'] = str(tweet.created_at)
            detailsDict['text'] = tweet.text
            tweetDict[key] = detailsDict
            detailsDict = {}
            count += 1
        f = open(file, 'w')
        json.dump(tweetDict, f)
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
            self._clear()
            print(viewTweets(self.userName))
            h = input('\n\n PRESS ENTER KEY TO GO BACK')
            self._clear()
            self.view()

        # 3. View words ranks
        if page == 3:
            self._clear()
            print(viewRanks())
            h = input('\n\n PRESS ENTER KEY TO GO BACK')
            self._clear()
            self.view()

        # 4. View sentiments analysis
        if page == 4:
            self._clear()
            print(viewSentiments())
            h = input('\n\n PRESS ENTER KEY TO GO BACK')
            self._clear()
            self.view()


def main():
    t = Tweet()
    t.prompt()

    try:
        # validate the user name
        t.validateUser(t.userName)

        # welcome user
        print(user_prompts.welcome.format(t.userName))

        # obtain user tweets
        t.getTweets(t.userName, t.tweets)

        # check if file exsist. create if doesn't and clean if exsists
        t.exist(t.jsonFile)

        # dump to json file
        t.dumpJson(t.userTweets, t.jsonFile)

        # ask user what to view
        t.view()

    except tweepy.TweepError as t:
        print(t.args[0])

if __name__ == '__main__':
    main()
