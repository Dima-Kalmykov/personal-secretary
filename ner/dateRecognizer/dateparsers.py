#!/usr/bin/env python
# encoding: utf-8
"""
timeparsers.py
"""

from ner.dateRecognizer.utils import dateparsers as dp
from ner.dateRecognizer.utils import dateregexp as dr


def getAllParsers(dict):
    # Стандартное написание даты через сепаратор
    parsersStandart = list(map(
        lambda sep: dp.getStandardDateParser(sep),
        dr.DATE_SEPARATORS
    )) * 2

    # Стандартное написание даты с приписным месяцем
    parsersWrittenMonth = [
        dp.getWrittenMonthParser(dict)
    ] * 4

    # Написание даты с приписным днем и месяцем
    parsersWrittenDayMonth = [
        dp.getWrittenDayMonthParser(dict)
    ] * 4 * 4

    parsersConst = [
        dp.todayParse,
        dp.theDayAfterTomorrowParse,
        dp.tomorrowParse,
        dp.weekendsParse,
    ]

    # День недели на следующей неделе
    parsersDayOfWeekNextWeek = [
        dp.getOnWeekDayNextWeekParser(dict)
    ] * 6 * 2

    # В n-ых числах месяца
    parsersNumbersInSpecificMonth = [
        dp.getInNumbersOfMonthsParser(dict)
    ]

    parsersNext = [
        dp.nextWeekParse,
        dp.nextMonthParse,
    ]

    # День недели
    parsersDayOfWeek = [
        dp.getDayOfWeekParser(dict)
    ] * 6

    # Через n дней
    parsersInDays = [
        dp.getInDaysParser(dict)
    ] * 2

    # Через n недель
    parsersInWeeks = [
        dp.getInWeeksParser(dict)
    ] * 2

    # Через n месяцев
    parsersInMonths = [
        dp.getInMonthsParser(dict)
    ] * 2

    # Через n лет
    parsersInYears = [
        dp.getInYearsParser(dict)
    ] * 2

    # В каком-то месяце
    parsersInSpecificMonth = [
        dp.getInSpecificMonthParser(dict)
    ] * 5

    parsers = parsersStandart + \
        parsersWrittenMonth + \
        parsersWrittenDayMonth + \
        parsersConst + \
        parsersDayOfWeekNextWeek + \
        parsersNumbersInSpecificMonth + \
        parsersNext + \
        parsersDayOfWeek + \
        parsersInDays + \
        parsersInWeeks + \
        parsersInMonths + \
        parsersInYears + \
        parsersInSpecificMonth

    return parsers
