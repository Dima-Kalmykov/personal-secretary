#!/usr/bin/env python
# encoding: utf-8
"""
timeregexp.py
"""

import re
from ner.timeRecognizer.utils import timeregexp as tr

cases = ['im', 'rod', 'dat']


def getAllRegexps(numbers_map):
    # Стандартное написание времени через сепаратор, до 12 часов включительно
    regexpsStandartMorning = list(map(
        lambda sep: '\\b' + tr.HOURS_1 + sep + tr.MINUTES + '\\b',
        tr.TIME_SEPARATORS
    ))

    # Стандартное написание времени через сепаратор, с 13 часов включительно + полночь / полдень
    regexpsStandartOther = list(map(
        lambda sep: '\\b' + tr.HOURS_2 + sep + tr.MINUTES + '\\b',
        tr.TIME_SEPARATORS
    )) + [
        tr.MIDNIGHT,
        tr.MIDDAY,
    ]

    # Половина чего-то
    regexpsHalf = [
        tr.getHalfRegexp(numbers_map)
    ]

    # Без скольки-то что-то (утро)
    regexpsWithoutMorning = [
        tr.getWithout(numbers_map, True, False, False, False),
        tr.getWithout(numbers_map, True, False, True, False),
        tr.getWithout(numbers_map, True, True, False, False),
        tr.getWithout(numbers_map, True, True, True, False),
        tr.getWithout(numbers_map, True, False, False, True),
        tr.getWithout(numbers_map, True, False, True, True),
        tr.getWithout(numbers_map, True, True, False, True),
        tr.getWithout(numbers_map, True, True, True, True),
    ]

    # Без скольки-то что-то (вечер)
    regexpsWithoutOther = [
        tr.getWithout(numbers_map, False, False, False, False),
        tr.getWithout(numbers_map, False, False, True, False),
        tr.getWithout(numbers_map, False, True, False, False),
        tr.getWithout(numbers_map, False, True, True, False),
        tr.getWithout(numbers_map, False, False, False, True),
        tr.getWithout(numbers_map, False, False, True, True),
        tr.getWithout(numbers_map, False, True, False, True),
        tr.getWithout(numbers_map, False, True, True, True),
    ]

    # n часов m минут (утро)
    regexpsHoursMinutesMorning = [
        tr.getHoursMinutes(numbers_map, True, False, False, False, None)
    ] + sum(list(map(lambda x: [
        tr.getHoursMinutes(numbers_map, True, False, True, False, x),
        tr.getHoursMinutes(numbers_map, True, True, False, False, x),
        tr.getHoursMinutes(numbers_map, True, True, True, False, x),
    ], cases)), []) + [
        tr.getHoursMinutes(numbers_map, True, False, False, True, None),
    ] + sum(list(map(lambda x: [
        tr.getHoursMinutes(numbers_map, True, False, True, True, x),
        tr.getHoursMinutes(numbers_map, True, True, False, True, x),
        tr.getHoursMinutes(numbers_map, True, True, True, True, x),
    ], cases)), [])

    # n часов m минут (вечер)
    regexpsHoursMinutesOther = [
        tr.getHoursMinutes(numbers_map, False, False, False, False, None),
    ] + sum(list(map(lambda x: [
        tr.getHoursMinutes(numbers_map, False, False, True, False, x),
        tr.getHoursMinutes(numbers_map, False, True, False, False, x),
        tr.getHoursMinutes(numbers_map, False, True, True, False, x),
    ], cases)), []) + [
        tr.getHoursMinutes(numbers_map, False, False, False, True, None),
    ] + sum(list(map(lambda x: [
        tr.getHoursMinutes(numbers_map, False, False, True, True, x),
        tr.getHoursMinutes(numbers_map, False, True, False, True, x),
        tr.getHoursMinutes(numbers_map, False, True, True, True, x),
    ], cases)), [])

    # n часов (утро)
    regexpsHoursOnlyMorning = [
        tr.getHoursOnly(numbers_map, True, False, None)
    ] + list(map(lambda x: tr.getHoursOnly(numbers_map, True, True, x), cases))

    # n часов (вечер)
    regexpsHoursOnlyOther = [
        tr.getHoursOnly(numbers_map, False, False, None)
    ] + list(map(lambda x: tr.getHoursOnly(numbers_map, False, True, x), cases))

    # m минут n-ого (утро)
    regexpsMinutesOfMorning = [
        tr.getMinutesOf(numbers_map, True, False, False, False, None),
    ] + sum(list(map(lambda x: [
        tr.getMinutesOf(numbers_map, True, False, True, False, x),
        tr.getMinutesOf(numbers_map, True, True, False, False, x),
        tr.getMinutesOf(numbers_map, True, True, True, False, x),
    ], cases)), []) + [
        tr.getMinutesOf(numbers_map, True, False, False, True, None),
    ] + sum(list(map(lambda x: [
        tr.getMinutesOf(numbers_map, True, False, True, True, x),
        tr.getMinutesOf(numbers_map, True, True, False, True, x),
        tr.getMinutesOf(numbers_map, True, True, True, True, x),
    ], cases)), [])

    # m минут n-ого (вечер)
    regexpsMinutesOfOther = [
        tr.getMinutesOf(numbers_map, False, False, False, False, None),
    ] + sum(list(map(lambda x: [
        tr.getMinutesOf(numbers_map, False, False, True, False, x),
        tr.getMinutesOf(numbers_map, False, True, False, False, x),
        tr.getMinutesOf(numbers_map, False, True, True, False, x),
    ], cases)), []) + [
        tr.getMinutesOf(numbers_map, False, False, False, True, None),
    ] + sum(list(map(lambda x: [
        tr.getMinutesOf(numbers_map, False, False, True, True, x),
        tr.getMinutesOf(numbers_map, False, True, False, True, x),
        tr.getMinutesOf(numbers_map, False, True, True, True, x),
    ], cases)), [])

    # Время прописью (полностью, утро)
    regexpsWrittenExactMorning = [
        tr.getWrittenTimeRegexp('im', False, True, numbers_map),
        tr.getWrittenTimeRegexp('rod', False, True, numbers_map),
        tr.getWrittenTimeRegexp('dat', False, True, numbers_map),
        tr.getWrittenTimeRegexp('im', True, True, numbers_map),
        tr.getWrittenTimeRegexp('rod', True, True, numbers_map),
        tr.getWrittenTimeRegexp('dat', True, True, numbers_map),
    ]

    # Время прописью (полностью, вечер)
    regexpsWrittenExactOther = [
        tr.getWrittenTimeRegexp('im', False, False, numbers_map),
        tr.getWrittenTimeRegexp('rod', False, False, numbers_map),
        tr.getWrittenTimeRegexp('dat', False, False, numbers_map),
        tr.getWrittenTimeRegexp('im', True, False, numbers_map),
        tr.getWrittenTimeRegexp('rod', True, False, numbers_map),
        tr.getWrittenTimeRegexp('dat', True, False, numbers_map),
    ]

    # Время прописью (часы, утро)
    regexpsWrittenHoursMorning = [
        tr.getWrittenHourRegexp('im', True),
        tr.getWrittenHourRegexp('rod', True),
        tr.getWrittenHourRegexp('dat', True),
    ]

    # Время прописью (часы, вечер)
    regexpsWrittenHoursOther = [
        tr.getWrittenHourRegexp('im', False),
        tr.getWrittenHourRegexp('rod', False),
        tr.getWrittenHourRegexp('dat', False),
    ]

    # в/к/около n (часов/часам/часов) (утро)
    regexpsAtHourMorning = [
        tr.getAtHour(numbers_map, True, False, None),
        tr.getAtHour(numbers_map, True, True, 'im'),
        tr.getAtHour(numbers_map, True, True, 'rod'),
        tr.getAtHour(numbers_map, True, True, 'dat'),
    ]

    # в/к/около n (часов/часам/часов) (вечер)
    regexpsAtHourOther = [
        tr.getAtHour(numbers_map, False, False, None),
        tr.getAtHour(numbers_map, False, True, 'im'),
        tr.getAtHour(numbers_map, False, True, 'rod'),
        tr.getAtHour(numbers_map, False, True, 'dat'),
    ]

    # Время с уточнением "утра"
    regexpsInTheMorning = list(
        map(tr.getInTheMorning, regexpsStandartMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsHalf)
    ) + list(
        map(tr.getInTheMorning, regexpsWithoutMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsHoursMinutesMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsHoursOnlyMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsMinutesOfMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsWrittenExactMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsWrittenHoursMorning)
    ) + list(
        map(tr.getInTheMorning, regexpsAtHourMorning)
    )

    # Время с уточнением "дня"
    regexpsInTheDay = list(
        map(tr.getInTheDay, regexpsStandartMorning)
    ) + list(
        map(tr.getInTheDay, regexpsHalf)
    ) + list(
        map(tr.getInTheDay, regexpsWithoutMorning)
    ) + list(
        map(tr.getInTheDay, regexpsHoursMinutesMorning)
    ) + list(
        map(tr.getInTheDay, regexpsHoursOnlyMorning)
    ) + list(
        map(tr.getInTheDay, regexpsMinutesOfMorning)
    ) + list(
        map(tr.getInTheDay, regexpsWrittenExactMorning)
    ) + list(
        map(tr.getInTheDay, regexpsWrittenHoursMorning)
    ) + list(
        map(tr.getInTheDay, regexpsAtHourMorning)
    )

    # Время с уточнением "вечера"
    regexpsInTheEvening = list(
        map(tr.getInTheEvening, regexpsStandartMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsHalf)
    ) + list(
        map(tr.getInTheEvening, regexpsWithoutMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsHoursMinutesMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsHoursOnlyMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsMinutesOfMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsWrittenExactMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsWrittenHoursMorning)
    ) + list(
        map(tr.getInTheEvening, regexpsAtHourMorning)
    )

    # Время с уточнением "ночи"
    regexpsInTheNight = list(
        map(tr.getInTheNight, regexpsStandartMorning)
    ) + list(
        map(tr.getInTheNight, regexpsHalf)
    ) + list(
        map(tr.getInTheNight, regexpsWithoutMorning)
    ) + list(
        map(tr.getInTheNight, regexpsHoursMinutesMorning)
    ) + list(
        map(tr.getInTheNight, regexpsHoursOnlyMorning)
    ) + list(
        map(tr.getInTheNight, regexpsMinutesOfMorning)
    ) + list(
        map(tr.getInTheNight, regexpsWrittenExactMorning)
    ) + list(
        map(tr.getInTheNight, regexpsWrittenHoursMorning)
    ) + list(
        map(tr.getInTheNight, regexpsAtHourMorning)
    )

    regexps = regexpsInTheMorning + \
        regexpsInTheDay + \
        regexpsInTheEvening + \
        regexpsInTheNight + \
        regexpsStandartOther + \
        regexpsStandartMorning + \
        regexpsHalf + \
        regexpsWithoutOther + \
        regexpsWithoutMorning + \
        regexpsHoursMinutesOther + \
        regexpsHoursMinutesMorning + \
        regexpsHoursOnlyOther + \
        regexpsHoursOnlyMorning + \
        regexpsMinutesOfOther + \
        regexpsMinutesOfMorning + \
        regexpsWrittenExactOther + \
        regexpsWrittenExactMorning + \
        regexpsWrittenHoursOther + \
        regexpsWrittenHoursMorning + \
        regexpsAtHourOther + \
        regexpsAtHourMorning

    return regexps
