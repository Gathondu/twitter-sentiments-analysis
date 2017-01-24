"""This file store all the prompts that the console app will use
and also all the messages and banners.
"""

welcome = "Welcome @{} to your Twitter Status Sentiments Analysis"

user_name = "Enter your twitter account username (with/without '@'): "

tweets = """Enter the number of tweets to fetch.
Maximum number of tweets is 500 tweets: """

invalid_user = "The username you have provided doesn't exsist!"

invalid_tweets = """That input is invalid.
Please enter a number between 1 and 500: """

terminate = '''Do you want to enter another username or quit?
type 'q' to quit or any key to continue: '''

change_tweets = "Do you want to change the number of tweets to view? [Y]/n "

exit = "Goodbye {}{}!!! See you later!"

views = """Enter a number to depict how you would like to interact with the app.
e.g 1 will list for you the help menu.

        1. Help
        2. View Tweets
        3. View words ranks
        4. View sentiments analysis
"""

help = """ Welcome @{} to Twitter Sentiments Analysis help.

To quit the app, simply type q or quit at any interaction point
e.g typing quit instead of @username, quits the program. This applies
to quiting this help menu too.

View Tweets option lets you view a list of the random 20 tweets that you
tweeted and when they were tweeted.

View words rank lets you view a list of the words you have used in your tweets,
excluding stop words (an, the, but, and,...), having ranked them from the
highly used to the least used.

View sentiments analysis displays an analysis of your sentiments/mood of your
tweets depending on your choice of words in the tweet.

Have FUN!!
"""
