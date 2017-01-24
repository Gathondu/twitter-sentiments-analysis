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
        try:
            user = self.api.get_user(screen_name=name)
        except tweepy.TweepError:
            print(user_prompts.invalid_user)
            self.prompt()
            self.validateUser(self.userName)

    # functioin to validate number of tweets to fetch is valid
    def validateTweetNumber(self, number):
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

            if result not in ('n', 'no'):
                self._clear()
                self.tweets = input(user_prompts.tweets)
                self._clear()
                self.tweets = self.validateTweetNumber(self.tweets)

    def getTweets(self, user, number):
        # get user tweets
        self.userTweets = tweepy.Cursor(self.api.user_timeline,
                                        id=user).items(
                                        int(number))


def main():
    t = Tweet()
    t.prompt()

    try:
        # validate the user name
        t.validateUser(t.userName)

        # welcome user
        print(user_prompts.welcome.format(t.userName))

        t.getTweets(t.userName, t.tweets)

        # check if file exsist. create if doesn't and clean if exsists
        t.exist(t.jsonFile)

        # dump data to file
        count = 1
        tweetDict = {}
        for tweet in t.userTweets:
            key = "tweet" + str(count)
            tweetDict[key] = tweet.text
            count += 1
        f = open(t.jsonFile, 'w')
        json.dump(tweetDict, f)
        f.close()

    except tweepy.TweepError as t:
        print(t.args[0])

if __name__ == '__main__':
    main()
