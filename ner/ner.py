#!/usr/bin/env python
# encoding: utf-8
"""
ner.py
"""


import timeit
from ner.dateRecognizer.date import getDateRecognizer
from ner.personsRecognizer.persons import getPersonsRecognizer
from ner.summarization.summarization import getSummarizer
from ner.timeRecognizer.time import getTimeRecognizer
from ner.urlRecognizer.url import getUrlRecognizer
from ner.utils.prepare import prepareText


def getEventData(message, sendingDate, timeRecognizer, dateRecognizer, urlRecognizer, personsRecognizer, summarizer, senderName, isFromOneself):
    start = timeit.default_timer()

    print('-----Processing message-----')

    link = urlRecognizer(message)
    print('1/5 Link ready')

    preparedText = prepareText(message.replace(link, '') if link else message)

    time = timeRecognizer(preparedText)
    print('2/5 Time ready')

    date = dateRecognizer(
        preparedText, 
        sendingDate.replace(hour=0, minute=0, second=0, microsecond=0)
    )
    print('3/5 Date ready')
    persons = personsRecognizer(message)
    print('4/5 Persons ready')
    summarization = summarizer(senderName + ': ' + message)
    print('5/5 Summary ready')

    print('-----Processing finnished-----')

    stop = timeit.default_timer()

    print('\tTime: ', stop - start)

    persons = ['Вы'] + ([senderName] if not isFromOneself else []) + persons

    return {
        'text': summarization,
        'datetime': date + time,
        'link': link,
        'persons': persons,
    }


def getNerModel():
    print('Creating model...')

    timeRecognizer = getTimeRecognizer()
    print('1/5 Time model ready')

    dateRecognizer = getDateRecognizer()
    print('2/5 Date model ready')

    urlRecognizer = getUrlRecognizer()
    print('3/5 Link model ready')

    personsRecognizer = getPersonsRecognizer()
    print('4/5 Persons model ready')

    summarizer = getSummarizer()
    print('5/5 Summarizer ready')

    print('model ready')
    return lambda message, sendingDate, senderName, isFromOneself: getEventData(message, sendingDate, timeRecognizer, dateRecognizer, urlRecognizer, personsRecognizer, summarizer, senderName, isFromOneself)
