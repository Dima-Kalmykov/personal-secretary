#!/usr/bin/env python
# encoding: utf-8
"""
timeparsers.py
"""

import re
from datetime import timedelta
from ner.timeRecognizer.utils import timeregexp as tr

# Будем считать, что до 9 часы чаще всего воспринимаеются как часы дня(вечера)
# Н-р, говоря "в пять часов", мы скорее всего имеем в виду 17:00
START_OF_HOURS = 9


def getHours(td):
    return td.total_seconds() // 3600

# Стандартное указание на время (н-р 22:35)
def standartTimeParse(time, sep):
    h, m = list(map(int, time.split(sep[-1])))
    return timedelta(hours=h, minutes=m)


def getStandartTimeParser(sep):
    return lambda time: standartTimeParse(time, sep)


# Полночь
def getMidnight(_):
    return timedelta()

# Полдень
def getMidday(_):
    return timedelta(hours=12)


# Указание на время прописью (н-р десять ноль пять)
def writtenExactTimeParse(time, words):
    numbers = list(map(lambda x: words[x], time.split(' ')))
    if len(numbers) == 2:
        h, m = numbers
    elif len(numbers) == 4:
        h, m = numbers[0] + numbers[1], numbers[2] + numbers[3]
    else:
        h, m = [numbers[0] + numbers[1], numbers[2]
                ] if numbers[1] < 10 else [numbers[0], numbers[1] + numbers[2]]
    h = h + 12 if h > 0 and h < START_OF_HOURS else h
    return timedelta(hours=h, minutes=m)


def getWrittenExactTimeParser(words):
    return lambda time: writtenExactTimeParse(time, words)


# Указание на время прописью, только часы (н-р десять)
def writtenHourParse(time, words):
    time = re.sub('( часов| часа| часам)', '', time).strip()
    h = words[time]
    h = h + 12 if h > 0 and h < START_OF_HOURS else h
    return timedelta(hours=h)


def getWrittenHourParser(words):
    return lambda time: writtenHourParse(time, words)


# Любое указание на время с припиской "утра" => все что больше 12 маппим в первую половину дня
def inTheMorningParse(time, parser):
    time = time.replace(' утра', '')
    t = parser(time)
    if getHours(t) > 12:
        t = t - timedelta(hours=12)
    return t


def getInTheMorningParser(parser):
    return lambda time: inTheMorningParse(time, parser)


# Любое указание на время с припиской "дня" => все что меньше 13 маппим во вторую половину дня
def inTheDayParse(time, parser):
    time = time.replace(' дня', '')
    t = parser(time)
    if getHours(t) < 13:
        t = t + timedelta(hours=12)
    return t


def getInTheDayParser(parser):
    return lambda time: inTheDayParse(time, parser)


# Любое указание на время с припиской "вечера" => все что меньше 13 маппим во вторую половину дня
def inTheEveningParse(time, parser):
    time = time.replace(' вечера', '')
    t = parser(time)
    if getHours(t) < 13:
        t = t + timedelta(hours=12)
    return t


def getInTheEveningParser(parser):
    return lambda time: inTheEveningParse(time, parser)


# Любое указание на время с припиской "ночи" => все что больше 12 маппим в первую половину дня
def inTheNightParse(time, parser):
    time = time.replace(' ночи', '')
    t = parser(time)
    if getHours(t) > 12:
        t = t - timedelta(hours=12)
    return t


def getInTheNightParser(parser):
    return lambda time: inTheNightParse(time, parser)


# Половина чего-то
def halfParse(time, words):
    which_half = re.search(tr.WHICH_HALF, time)
    time = re.sub(
        tr.HALF, '',
        re.sub(tr.WHICH_HALF, '', time)
    ).strip()
    m = 30 if not which_half or which_half[0].startswith('в') else 0
    h = int(time) - 1 if time.isnumeric() else words[time] - 1
    h = h + 12 if h < START_OF_HOURS else h
    return timedelta(hours=h, minutes=m)


def getHalfParser(words):
    return lambda time: halfParse(time, words)


def withoutParse(time, words):
    time = re.sub(
        '( минут| минуты| мин)', '',
        re.sub('без ', '', time)
    ).strip()

    numbers = list(map(lambda x: int(x) if x.isnumeric()
                   else words[x], time.split(' ')))
    if len(numbers) == 2:
        m, h = numbers
    elif len(numbers) == 4:
        m, h = numbers[0] + numbers[1], numbers[2] + numbers[3]
    else:
        m, h = [numbers[0] + numbers[1], numbers[2]
                ] if numbers[1] < 10 else [numbers[0], numbers[1] + numbers[2]]

    h = h + 12 if h > 0 and h < START_OF_HOURS else h
    return timedelta(hours=h-1, minutes=60-m)


def getWithoutParser(words):
    return lambda time: withoutParse(time, words)


def hoursMinutesParse(time, words):
    time = re.sub(
        '( часов| часам| часу| часа| час)', '', time
    ).strip()

    if re.search('(минуту| минутам| минуте| минуты| минут)', time):
        time = re.sub('(минуту| минутам| минуте| минуты| минут)', '', time).strip()
        numbers = list(map(lambda x: int(x) if x.isnumeric()
                    else words[x], time.split(' ')))
        if len(numbers) == 1:
            h, m = numbers[0], 0
        elif len(numbers) == 2:
            h, m = numbers
        elif len(numbers) == 4:
            h, m = numbers[0] + numbers[1], numbers[2] + numbers[3]
        else:
            h, m = [numbers[0] + numbers[1], numbers[2]
                    ] if numbers[1] < 10 else [numbers[0], numbers[1] + numbers[2]]
    else:
        h, m = int(time) if time.isnumeric() else words[time], 0

    h = h + 12 if h > 0 and h < START_OF_HOURS else h
    return timedelta(hours=h, minutes=m)

def getHoursMinutesParser(words):
    return lambda time: hoursMinutesParse(time, words)

def minutesOfParse(time, words):
    time = re.sub(
        '( минутам| минута| минуте| минуты| минут| мин)', '', time
    )
    time = re.sub(
        '(минутам |минута |минуте |минуты |минут |мин )', '', time
    ).strip()

    numbers = list(map(lambda x: int(x) if x.isnumeric()
                   else words[x], time.split(' ')))
    if len(numbers) == 2:
        m, h = numbers
    elif len(numbers) == 4:
        m, h = numbers[0] + numbers[1], numbers[2] + numbers[3]
    else:
        m, h = [numbers[0] + numbers[1], numbers[2]
                ] if numbers[1] < 10 else [numbers[0], numbers[1] + numbers[2]]

    h = h + 12 if h > 0 and h < START_OF_HOURS else h
    return timedelta(hours=h-1, minutes=m)

def getMinutesOfParser(words):
    return lambda time: minutesOfParse(time, words)


def atHourParse(time, words):
    time = re.sub(
        '(в |к |около )', '', time
    )
    time = re.sub(
        '( часов| часам| часу| часа| час)', '', time
    ).strip()

    if time.isnumeric():
        h = int(time)
    else:
        h = words[time]

    h = h + 12 if h > 0 and h < START_OF_HOURS else h
    return timedelta(hours=h)

def getAtHourParser(words):
    return lambda time: atHourParse(time, words)
