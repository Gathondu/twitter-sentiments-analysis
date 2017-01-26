import user_prompts
import tweepy
import tweet_tables

from time import sleep
from tweet import Tweet


def main():
    t = Tweet()
    t.prompt()

    try:
        # validate the user name
        t.validateUser(t.userName)
        t._clear()
        # obtain user tweets
        t.getTweets(t.userName)
        # t.progress(20, 'obtaining @{} tweets'.format(t.userName), 0.5)

        # check if file exsist. create if doesn't and clean if exsists
        t.exist(t.jsonFile)

        # dump to json file
        t.dumpJson(t.jsonFile)
        print("Complete!!")

        sleep(0.5)
        t._clear()
        # welcome user
        print(user_prompts.welcome.format(t.userName))

        # ask user what to view
        t.view()

    except tweepy.TweepError as t:
        print(t.args[0])

if __name__ == '__main__':
    main()
