#!/usr/bin/env python
# encoding: utf-8
"""
dateparsers.py
"""

from ner.timeRecognizer.utils import timeparsers as tp
from ner.timeRecognizer.utils import timeregexp as tr


def getAllParsers(numbers_map):
    # Стандартное написание времени через сепаратор
    parsersStandart = list(map(
        tp.getStandartTimeParser,
        tr.TIME_SEPARATORS
    ))

    # полночь / полдень
    parsersMid = [
        tp.getMidnight,
        tp.getMidday
    ]

    # половина чего-то
    parsersHalf = [
        tp.getHalfParser(numbers_map)
    ]

    # Без скольки-то что-то
    parsersWithout = [
        tp.getWithoutParser(numbers_map)
    ] * 8

    # n часов m минут
    parsersHoursMinutes = [
        tp.getHoursMinutesParser(numbers_map)
    ] * 24

    # m минут n-ого
    parsersMinutesOf = [
        tp.getMinutesOfParser(numbers_map)
    ] * 20

    # Время прописью (полностью)
    parsersWrittenExact = [
        tp.getWrittenExactTimeParser(numbers_map)
    ] * 6  # потому что регулярок на этот парсер 2 списка по 6

    # Время прописью (часы)
    parsersWrittenHours = [
        tp.getWrittenHourParser(numbers_map)
    ] * 3  # потому что регулярок на этот парсер 2 списка по 3

    # в/к/около n (часов/часам/часов)
    parsersAtHour = [
        tp.getAtHourParser(numbers_map)
    ] * 4

    # Время с уточнением "утра"
    parsersInTheMorning = list(
        map(tp.getInTheMorningParser, parsersStandart)
    ) + list(
        map(tp.getInTheMorningParser, parsersHalf)
    ) + list(
        map(tp.getInTheMorningParser, parsersWithout)
    ) + list(
        map(tp.getInTheMorningParser, parsersHoursMinutes)
    ) + list(
        map(tp.getInTheMorningParser, parsersMinutesOf)
    ) + list(
        map(tp.getInTheMorningParser, parsersWrittenExact)
    ) + list(
        map(tp.getInTheMorningParser, parsersWrittenHours)
    ) + list(
        map(tp.getInTheMorningParser, parsersAtHour)
    )

    # Время с уточнением "дня"
    parsersInTheDay = list(
        map(tp.getInTheDayParser, parsersStandart)
    ) + list(
        map(tp.getInTheDayParser, parsersHalf)
    ) + list(
        map(tp.getInTheDayParser, parsersWithout)
    ) + list(
        map(tp.getInTheDayParser, parsersHoursMinutes)
    ) + list(
        map(tp.getInTheDayParser, parsersMinutesOf)
    ) + list(
        map(tp.getInTheDayParser, parsersWrittenExact)
    ) + list(
        map(tp.getInTheDayParser, parsersWrittenHours)
    ) + list(
        map(tp.getInTheDayParser, parsersAtHour)
    )

    # Время с уточнением "вечера"
    parsersInTheEvening = list(
        map(tp.getInTheEveningParser, parsersStandart)
    ) + list(
        map(tp.getInTheEveningParser, parsersHalf)
    ) + list(
        map(tp.getInTheEveningParser, parsersWithout)
    ) + list(
        map(tp.getInTheEveningParser, parsersHoursMinutes)
    ) + list(
        map(tp.getInTheEveningParser, parsersMinutesOf)
    ) + list(
        map(tp.getInTheEveningParser, parsersWrittenExact)
    ) + list(
        map(tp.getInTheEveningParser, parsersWrittenHours)
    ) + list(
        map(tp.getInTheEveningParser, parsersAtHour)
    )

    # Время с уточнением "ночи"
    parsersInTheNight = list(
        map(tp.getInTheNightParser, parsersStandart)
    ) + list(
        map(tp.getInTheNightParser, parsersHalf)
    ) + list(
        map(tp.getInTheNightParser, parsersWithout)
    ) + list(
        map(tp.getInTheNightParser, parsersHoursMinutes)
    ) + list(
        map(tp.getInTheNightParser, parsersMinutesOf)
    ) + list(
        map(tp.getInTheNightParser, parsersWrittenExact)
    ) + list(
        map(tp.getInTheNightParser, parsersWrittenHours)
    ) + list(
        map(tp.getInTheNightParser, parsersAtHour)
    )

    parsers = parsersInTheMorning + \
        parsersInTheDay + \
        parsersInTheEvening + \
        parsersInTheNight + \
        parsersStandart + \
        parsersMid + \
        parsersStandart + \
        parsersHalf + \
        parsersWithout + \
        parsersWithout + \
        parsersHoursMinutes + \
        parsersHoursMinutes + \
        parsersMinutesOf + \
        parsersMinutesOf + \
        parsersWrittenExact + \
        parsersWrittenExact + \
        parsersWrittenHours + \
        parsersWrittenHours + \
        parsersAtHour + \
        parsersAtHour

    return parsers
