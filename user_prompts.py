"""This file store all the prompts that the console app will use
and also all the messages and banners.
"""

welcome = "{} to your Twitter Status Sentiments Analysis"

user_name = "Enter your twitter account username (with/without '@'): "

period = """Enter the period in weeks, from which to fetch data.
Maximum number of weeks is 8 weeks: """

invalid_user = "The username you have provided doesn't exsist!"

invalid_period = """That period is invalid.
Please enter a number between 0 and 8: """

terminate = '''Do you want to enter another username or quit?
type 'q' to quit or any key to continue: '''
