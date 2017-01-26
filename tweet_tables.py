import json
import re

from terminaltables import SingleTable
from colorclass import Color
from textwrap import wrap
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from tqdm import tqdm


def getStopwords():
    return set(stopwords.words('english'))


def getFile():
    return json.load(open('tweets.json'))


def viewTweets(username, number):
    twits = getFile()
    # create table
    table = [[Color('{autocyan}TWEET:{/autocyan}'),
              Color('{autored}POSTED ON:{/autored}')]]
    table_instance = SingleTable(table, Color('{green}' +
                                              '@'+username+'{/green}'))

    count = 1
    for twit in twits.items():
        if count > int(number):
            continue
        table.append(
            [
                Color('{autocyan}' +
                      '\n'.join(wrap(twit[1]["tweet"], 80)) +
                      '{/autocyan}'),
                Color('{autored}'+twit[1]["date"]+'{/autored}')
                ])
        count += 1
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'left', 1: 'left'}
    return table_instance.table


def viewRanks(number):
    twits = getFile()
    stopWords = getStopwords()
    words = []
    for twit in tqdm(twits.items(), total=number, desc="Ranking words..."):
        words.extend(word_tokenize(twit[1]['tweet']))
    words = [
        word for word in words if word.lower() not in stopWords and
        re.match(r'\w', word)
        ]
    wordsDict = Counter(words)
    sortedList = sorted(wordsDict.items(),
                        key=lambda x: x[1], reverse=True)
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


def viewSentiments(number):
    twits = getFile()
    table_data = [[Color('{cyan}TWEET{/cyan}'),
                   Color('{autored}SENTIMENTS{/autored}')]]
    table_instance = SingleTable(table_data,
                                 Color(
                                  '{green}Sentiment Analysis{/green}'))
    for twit in tqdm(twits.items(), total=number,
                     desc="Analysing sentiments..."):
        sentiment = twit[1]['sentiments']
        sentString = ''
        for item in sentiment:
            sentString += item + '\n'
        sentString = sentString.strip()
        table_data.append(
            [
                Color('{cyan}' +
                      '\n'.join(wrap(twit[1]['tweet'], 80))+'{/cyan}'),
                Color('{red}' + sentString + '{/red}')
            ]
        )
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'left', 1: 'left'}
    return table_instance.table
