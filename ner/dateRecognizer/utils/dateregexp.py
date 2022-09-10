#!/usr/bin/env python
# encoding: utf-8
"""
dateregexp.py
"""
import pandas as pd


DATE_SEPARATORS = ['\.', '/', '-', ' ']

PATH_TO_DATE = 'ner/dateRecognizer/date.csv'

DAY = '([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])'
MONTH = '([1-9]|0[1-9]|1[0-2])'
YEAR = '(20)?(2[2-9]|[3-9][0-9])'

TODAY = 'сегодня'
TOMORROW = 'завтра'
THE_DAY_AFTER_TOMORROW = '(послезавтра|после завтра)'
WEEKENDS = '(выходные|выходных|выхи|выхах)'
NEXT_WEEK = '(следующая|следующей|следущая|следущей|след|некст) (неделя|неделе|недели|неделей|нед)'
NEXT_MONTH = '(следующий|следующему|следущий|следущему|следущем|след|некст) (месяце|месяца|месяцу|месяцем|месяц|мес)'

def saveWords(dict, keys, values):
    for i in range(len(keys)):
        dict[keys[i]] = int(values[i])

def getStandardDateRegexp(separator):
    return '\\b' + DAY + separator + MONTH + separator + YEAR + '\\b'


def getStandardShortDateRegexp(separator):
    return '\\b' + DAY + separator + MONTH + '\\b'


def getWrittenMonthRegexp(dict, short):
    dt = pd.read_csv(PATH_TO_DATE, sep=';')
    months = dt['month_short' if short else 'month_rod'][:12]
    saveWords(dict, months, dt['number'])
    months = '|'.join(months)
    return '\\b' + DAY + ' (' + months + ') ' + YEAR + '\\b'


def getShortWrittenMonthRegexp(short):
    column = 'month_short' if short else 'month_rod'
    months = '|'.join(pd.read_csv(PATH_TO_DATE, sep=';')[column][:12])
    return '\\b' + DAY + ' (' + months + ')\\b'


def getWrittenDayMonthRegexp(dict, case, short):
    dt = pd.read_csv(PATH_TO_DATE, sep=';')
    months = '|'.join(dt['month_short' if short else 'month_rod'][:12])
    dates = dt['date_' + case]
    saveWords(dict, dates, dt['number'])
    dates = '|'.join(dates)
    return '\\b' + '(' + dates + ') (' + months + ') ' + YEAR + '\\b'


def getShortWrittenDayMonthRegexp(case, short):
    dt = pd.read_csv(PATH_TO_DATE, sep=';')
    months = '|'.join(dt['month_short' if short else 'month_rod'][:12])
    dates = '|'.join(dt['date_' + case])
    return '\\b' + '(' + dates + ') (' + months + ')\\b'


def getDayOfWeekRegexp(dict, case):
    days = pd.read_csv(PATH_TO_DATE, sep=';')['day_of_week_' + case][:7]
    saveWords(dict, days, range(1, 8))
    days = '|'.join(days)
    return '\\b(' + days + ')\\b'


def getInDaysRegexp(dict, written):
    if written:
        dt = pd.read_csv(PATH_TO_DATE, sep=';')
        days = list(map(str, dt['number_of_days']))
        saveWords(dict, days, dt['number'])
        days = '(' + '|'.join(days) + ')'
    else:
        days = '([1-9][0-9]*)'
    return 'через ?' + days + '? (дней|дня|день) ?' + days + '?'


def getInWeeksRegexp(dict, written):
    if written:
        dt = pd.read_csv(PATH_TO_DATE, sep=';')
        weeks = list(map(str, dt['number_of_weeks']))
        saveWords(dict, weeks, dt['number'])
        weeks = '(' + '|'.join(weeks) + ')'
    else:
        weeks = '([1-9][0-9]*)'
    return 'через ?' + weeks + '? (недель|недель|неделю|нед) ?' + weeks + '?'


def getInMonthsRegexp(dict, written):
    if written:
        dt = pd.read_csv(PATH_TO_DATE, sep=';')
        months = list(map(str, dt['number_of_days']))
        saveWords(dict, months, dt['number'])
        months = '(' + '|'.join(months) + ')'
    else:
        months = '([1-9][0-9]*)'
    return 'через ?' + months + '? (месяцев|месяца|месяц|мес) ?' + months + '?'

def getInYearsRegexp(dict, written):
    if written:
        dt = pd.read_csv(PATH_TO_DATE, sep=';')
        years = list(map(str, dt['number_of_days']))
        saveWords(dict, years, dt['number'])
        years = '(' + '|'.join(years) + ')'
    else:
        years = '([1-9][0-9]*)'
    return 'через ?' + years + '? (года|год|лет) ?' + years + '?'


def getOnWeekDayNextWeekRegexp(dict, case):
    days = pd.read_csv(PATH_TO_DATE, sep=';')['day_of_week_' + case][:7]
    saveWords(dict, days, range(1, 8))
    days = '|'.join(days)
    return '\\b(' + days + ')\\b' + '.*' + NEXT_WEEK + '\\b'


def getNextWeekOnWeekDayRegexp(case):
    days = pd.read_csv(PATH_TO_DATE, sep=';')['day_of_week_' + case][:7]
    days = '|'.join(days)
    return '\\b' + NEXT_WEEK + '.*\\b(' + days + ')\\b'


def getInSpecificMonthRegexp(dict, case):
    dt = pd.read_csv(PATH_TO_DATE, sep=';')
    months = dt['month_' + case][:12]
    saveWords(dict, months, dt['number'])
    months = '|'.join(months)
    return '\\b(' + months + ')\\b'


def getInNumbersOfMonthsRegexp():
    dt = pd.read_csv(PATH_TO_DATE, sep=';')
    months = '|'.join(dt['month_rod'][:12])
    thisAndNext = '(этого|следующего|следущего|след|некст)? ?месяца'
    numbers = '(перв|десят|двадцат|тридцат|[1-3]0)(х|ых)?'
    return '\\b'+ numbers +' числах (' + months + '|'+ thisAndNext +')\\b'
