#!/usr/bin/env python
# encoding: utf-8
"""
dateparsers.py
"""

from calendar import monthrange
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import re


def fixDayOverflow(y, m, d):
    maxDay = monthrange(y, m)[1]
    if d > maxDay:
        m = m + 1
        d = d - maxDay
    if m > 12:
        y = y + 1
        m = 1
    return y, m, d

def todayParse(_, today):
    return today


def tomorrowParse(_, today):
    return today + timedelta(days=1)


def theDayAfterTomorrowParse(_, today):
    return today + timedelta(days=2)


def weekendsParse(_, today):
    weekday = today.isoweekday()
    if weekday < 6:
        return today + timedelta(days=6-weekday)
    return today + timedelta(days=13-weekday)


def nextWeekParse(_, today):
    dayOfTheWeek = today.isoweekday()
    return today + timedelta(days=8-dayOfTheWeek)


def nextMonthParse(_, today):
    return today + relativedelta(days=-today.day+1, months=+1)


def standardDateParse(date, sep, today):
    numbers = list(map(int, date.split(sep[-1])))
    if len(numbers) == 3:
        d, m, y = numbers
    else:
        d, m = numbers
        y = today.year
    y = 2000 + y if y < 2000 else y
    y, m, d = fixDayOverflow(y, m, d)
    return datetime(y, m, d)


def getStandardDateParser(sep):
    return lambda date, today: standardDateParse(date, sep, today)


def writtenMonthParse(date, dict, today):
    values = date.split()
    d = int(values[0])
    m = dict[values[1]]
    y = int(values[2]) if len(values) > 2 else today.year
    y = 2000 + y if y < 2000 else y
    y, m, d = fixDayOverflow(y, m, d)
    return datetime(y, m, d)


def getWrittenMonthParser(dict):
    return lambda date, today: writtenMonthParse(date, dict, today)


def writtenDayMonthParse(date, dict, today):
    values = date.split()
    if len(values) == 2:
        d = dict[values[0]]
        m = dict[values[1]]
        y = today.year
    elif len(values) == 3:
        if values[-1] in dict:
            d = dict[values[0] + ' ' + values[1]]
            m = dict[values[2]]
            y = today.year
        else:
            d = dict[values[0]]
            m = dict[values[1]]
            y = int(values[2])
    else:
        d = dict[values[0] + ' ' + values[1]]
        m = dict[values[2]]
        y = int(values[3])
    y, m, d = fixDayOverflow(y, m, d)
    return datetime(y, m, d)


def getWrittenDayMonthParser(dict):
    return lambda date, today: writtenDayMonthParse(date, dict, today)


def dayOfWeekParse(date, dict, today):
    dayOfWeek = dict[date]
    todayOfWeek = today.isoweekday()
    delta = dayOfWeek - todayOfWeek if todayOfWeek < dayOfWeek else dayOfWeek - todayOfWeek + 7
    return today + timedelta(days=delta)


def getDayOfWeekParser(dict):
    return lambda date, today: dayOfWeekParse(date, dict, today)


def onWeekDayNextWeekParse(date, dict, today):
    date = re.sub(
        '(следующая|следующей|следущая|следущей|след|некст) (неделя|неделе|недели|неделей|нед)', '', date).strip()
    day = re.search(
        '(понедельник|вторник|сред|четверг|пятниц|суббот|воскресень|пн|вт|ср|чт|пт)', date)[0]
    if 'ср' in day:
        day = 3
    elif 'пят' in day:
        day = 5
    elif 'суб' in day:
        day = 6
    elif 'вос' in day:
        day = 7
    else:
        day = dict[day]
    return today + timedelta(days=day-today.isoweekday(), weeks=1)


def getOnWeekDayNextWeekParser(dict):
    return lambda date, today: onWeekDayNextWeekParse(date, dict, today)


def inDaysParse(date, dict, today):
    date = date.replace('через', '')
    date = re.sub('(дней|дня|день)', '', date).strip()
    if date == '':
        return today + timedelta(days=1)
    date = date.split()[0]
    delta = int(date) if date.isnumeric() else dict[date]
    return today + timedelta(days=delta)


def getInDaysParser(dict):
    return lambda date, today: inDaysParse(date, dict, today)


def inWeeksParse(date, dict, today):
    date = date.replace('через', '')
    date = re.sub('(недель|недель|неделю|нед)', '', date).strip()
    if date == '':
        return today + timedelta(weeks=1)
    date = date.split()[0]
    delta = int(date) if date.isnumeric() else dict[date]
    return today + timedelta(weeks=delta)


def getInWeeksParser(dict):
    return lambda date, today: inWeeksParse(date, dict, today)


def inMonthsParse(date, dict, today):
    date = date.replace('через', '')
    date = re.sub('(месяцев|месяца|месяц|мес)', '', date).strip()
    if date == '':
        return today + relativedelta(months=+1)
    date = date.split()[0]
    delta = int(date) if date.isnumeric() else dict[date]
    return today + relativedelta(months=+delta)


def getInMonthsParser(dict):
    return lambda date, today: inMonthsParse(date, dict, today)


def inYearsParse(date, dict, today):
    date = date.replace('через', '')
    date = re.sub('(года|год|лет)', '', date).strip()
    if date == '':
        return today + relativedelta(years=+1)
    date = date.split()[0]
    delta = int(date) if date.isnumeric() else dict[date]
    return today + relativedelta(years=+delta)


def getInYearsParser(dict):
    return lambda date, today: inYearsParse(date, dict, today)


def inSpecificMonthParse(date, dict, today):
    month = dict[date]
    year = today.year if today.month < month else today.year + 1
    return datetime(year, month, 1)


def getInSpecificMonthParser(dict):
    return lambda date, today: inSpecificMonthParse(date, dict, today)


def inNumbersOfMonthsParse(date, dict, today):
    numbers = re.search('(перв|десят|двадцат|тридцат|[1-3]0)(х|ых)?', date)[0]
    date = re.sub('(перв|десят|двадцат|тридцат|[1-3]0)(х|ых)? числах', '',
                  date).replace('месяца', '').strip()
    if re.search('следующего|следущего|след|некст', date):
        month = today.month + 1
    elif re.search('этого', date) or date not in dict:
        month = today.month
    else:
        month = dict[date]
    if 'перв' in numbers:
        day = 1
    elif '10' in numbers or 'десят' in numbers:
        day = 10
    elif '20' in numbers or 'двадцат' in numbers:
        day = 20
    else:
        day = 30
    year = today.year if month <= 12 else today.year + 1
    if today.month > month:
        year = year + 1
    maxDay = monthrange(year, month)[1]
    if day > maxDay:
        day = maxDay
    return datetime(year, (month - 1) % 12 + 1, day)


def getInNumbersOfMonthsParser(dict):
    return lambda date, today: inNumbersOfMonthsParse(date, dict, today)
