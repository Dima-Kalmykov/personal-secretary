#!/usr/bin/env python
# encoding: utf-8
"""
dateregexp.py
"""

import re
from ner.dateRecognizer.utils import dateregexp as dr

DAY_CASES = ['im', 'rod', 'dat', 'tv']
DAY_OF_WEEK_CASES = ['im', 'rod', 'dat', 'vin', 'tv', 'short']
MONTH_CASES = ['im', 'rod', 'dat', 'pred', 'short']


def getAllRegexps(dict):
    # Стандартное написание даты через сепаратор
    regexpsStandart = list(map(
        lambda sep: dr.getStandardDateRegexp(sep),
        dr.DATE_SEPARATORS
    )) + list(map(
        lambda sep: dr.getStandardShortDateRegexp(sep),
        dr.DATE_SEPARATORS
    ))

    # Стандартное написание даты с приписным месяцем
    regexpsWrittenMonth = [
        dr.getWrittenMonthRegexp(dict, False),
        dr.getWrittenMonthRegexp(dict, True),
        dr.getShortWrittenMonthRegexp(False),
        dr.getShortWrittenMonthRegexp(True),
    ]

    # Написание даты с приписным днем и месяцем
    regexpsWrittenDayMonth = list(map(
        lambda case: dr.getWrittenDayMonthRegexp(dict, case, False),
        DAY_CASES
    )) + list(map(
        lambda case: dr.getShortWrittenDayMonthRegexp(case, False),
        DAY_CASES
    )) + list(map(
        lambda case: dr.getWrittenDayMonthRegexp(dict, case, True),
        DAY_CASES
    )) + list(map(
        lambda case: dr.getShortWrittenDayMonthRegexp(case, True),
        DAY_CASES
    ))

    regexpsConst = [
        '\\b' + dr.TODAY + '\\b',
        '\\b' + dr.THE_DAY_AFTER_TOMORROW + '\\b',
        '\\b' + dr.TOMORROW + '\\b',
        '\\b' + dr.WEEKENDS + '\\b',
    ]

    # День недели на следующей неделе
    regexpsDayOfWeekNextWeek = list(map(
        lambda case: dr.getOnWeekDayNextWeekRegexp(dict, case),
        DAY_OF_WEEK_CASES
    )) + list(map(
        lambda case: dr.getNextWeekOnWeekDayRegexp(case),
        DAY_OF_WEEK_CASES
    ))

    regexpsNext = [
        '\\b' + dr.NEXT_WEEK + '\\b',
        '\\b' + dr.NEXT_MONTH + '\\b',
    ]

    # День недели
    regexpsDayOfWeek = list(map(
        lambda case: dr.getDayOfWeekRegexp(dict, case),
        DAY_OF_WEEK_CASES
    ))

    # Через n дней
    regexpsInDays = [
        dr.getInDaysRegexp(dict, False),
        dr.getInDaysRegexp(dict, True)
    ]

    # Через n недель
    regexpsInWeeks = [
        dr.getInWeeksRegexp(dict, False),
        dr.getInWeeksRegexp(dict, True)
    ]

    # Через n месяцев
    regexpsInMonths = [
        dr.getInMonthsRegexp(dict, False),
        dr.getInMonthsRegexp(dict, True)
    ]

    # Через n лет
    regexpsInYears = [
        dr.getInYearsRegexp(dict, False),
        dr.getInYearsRegexp(dict, True)
    ]

    # В n-ых числах месяца
    regexpsNumbersInSpecificMonth = [
        dr.getInNumbersOfMonthsRegexp()
    ]

    # В каком-то месяце
    regexpsInSpecificMonth = list(map(
        lambda case: dr.getInSpecificMonthRegexp(dict, case),
        MONTH_CASES
    ))

    regexps = regexpsStandart + \
        regexpsWrittenMonth + \
        regexpsWrittenDayMonth + \
        regexpsConst + \
        regexpsDayOfWeekNextWeek + \
        regexpsNumbersInSpecificMonth + \
        regexpsNext + \
        regexpsDayOfWeek + \
        regexpsInDays + \
        regexpsInWeeks + \
        regexpsInMonths + \
        regexpsInYears + \
        regexpsInSpecificMonth

    return regexps
