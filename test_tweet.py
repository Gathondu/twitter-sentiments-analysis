import unittest

from tweet import *


class TestTweet(unittest.TestCase):

    def setUp(self):
        # initialize global variables for the test class
        self.tweet = Tweet()

    # use mock to test function requiring input
    @mock.patch('tweet.prompt', return_value='@IDIOCRATE')
    def test_input_allows_utf_char(self, input):
        self.assertEquals(self.prompt(), 'IDIOCRATE_', "Input should allow @ char!")

    @skip('WIP')
    def test_input_throws_TweepError(self):
        with self.assertRaises(TweepError):
            self.tweet.prompt
