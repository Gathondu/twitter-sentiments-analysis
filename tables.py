import json
import tqdm

from terminaltables import SingleTable
from colorclass import Color
from textwrap import wrap
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentiments import getSentiment
from tweet import Tweet
from collections import Counter


def getStopwords():
    return set(stopwords.words('english'))


def getFile():
    return json.load(open('tweets.json'))


def viewTweets(username):
    twits = tqdm(getFile())
    # create table
    table = [[Color('{autocyan}TWEET:{/autocyan}'),
             Color('{autored}POSTED ON:{/autored}')]]
    table_instance = SingleTable(table, Color('{green}' +
                                              '@'+username+'{/green}'))

    count = 1
    for twit in tqdm(twits.items()):
        if count > 20:  # return latest 20 tweets
            continue
        table.append(
            [
                Color('{autocyan}' +
                      '\n'.join(wrap(twit[1]["text"], 80)) +
                      '{/autocyan}'),
                Color('{autored}'+twit[1]["date"]+'{/autored}')
                ])
        count += 1
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'left', 1: 'left'}
    return table_instance.table


def viewRanks():
    twits = getFile()
    stopWords = getStopwords()
    words = []
    for twit in twits.items():
        words.extend(word_tokenize(twit[1]['text']))
    words = [word for word in words if word.lower() not in stopWords]
    wordsDict = Counter(words)
    sortedList = sorted(wordsDict.items(), key=lambda x: x[1], reverse=True)
    table_data = [[Color('WORDS'), Color('{autored}RANKS{/autored}')]]
    for word in sortedList:
        table_data.append(
            [
                Color(word[0]),
                Color('{autored}' + str(word[1]) + '{/autored}')
            ]
        )
    table_instance = SingleTable(table_data,
                                 Color('{green}Word Frequency{/green}'))
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'center', 1: 'center'}
    return table_instance.table


def viewSentiments():
    twits = getFile()
    table_data = [[Color('{cyan}TWEET{/cyan}'),
                  Color('{autored}SENTIMENTS{/autored}')]]
    table_instance = SingleTable(table_data,
                                 Color('{green}Sentiment Analysis{/green}'))
    for twit in twits.items():
        sentiment = getSentiment(twit[1]['text'])
        sentString = ''
        for item in sentiment:
            sentString += item + '\n'
        sentString = sentString.strip()
        table_data.append(
            [
             Color('{cyan}'+'\n'.join(wrap(twit[1]['text'], 80))+'{/cyan}'),
             Color('{red}' + sentString + '{/red}')
            ]
        )
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'left', 1: 'left'}
    return table_instance.table
