import unittest
import tweepy

from tweet import *


class TestTweet(unittest.TestCase):

    def setUp(self):
        # initialize global variables for the test class
        self.tweet = Tweet()

    def test_input_throws_TweepError(self):
        with self.assertRaises(Error):
            self.tweet.prompt('@456dfr')
