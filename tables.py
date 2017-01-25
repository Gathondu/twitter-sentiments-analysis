import json

from terminaltables import SingleTable
from colorclass import Color
from textwrap import wrap


def viewTweets(username):
    twits = json.load(open('tweets.json'))
    # create table
    table = [[Color('{autocyan}Posted on:{/autocyan}'),
             Color('{autored}Tweet:{/autored}')]]
    table_instance = SingleTable(table, '@' + username)
    max_width = table_instance.column_max_width(1)

    count = 1
    for twit in twits.items():
        if count > 20:  # return latest 20 tweets
            continue
        table.append(
            [
                Color('{autored}'+twit[1]["date"]+'{/autored}'),
                Color('{autocyan}' +
                      '\n'.join(wrap(twit[1]["text"], max_width)) +
                      '{/autocyan}')
                ])
        count += 1
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'center', 1: 'center'}
    return table_instance.table


def viewRanks(wordsDict, stopwords):
    twits = json.load(open('tweets.json'))
    for twit in twits.items():
        words = twit[1]['text'].split()
        for word in words:
            if word not in stopwords:
                if word not in wordsDict.keys():
                    wordsDict[word] = 1
                else:
                    wordsDict[word] += 1
    table_data = [[Color('WORDS'), Color('{autored}RANKS{/autored}')]]
    for word in wordsDict.items():
        table_data.append(
            [
                Color(word[0]),
                Color('{autored}' + str(word[1]) + '{/autored}')
            ]
        )
    table_instance = SingleTable(table_data, 'Word Frequency')
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'center', 1: 'center'}
    return table_instance.table
