#!/usr/bin/env python
# encoding: utf-8
"""
timeregexp.py
"""
import pandas as pd

TIME_SEPARATORS = [':', ';', '\.', ' ']
WHICH_HALF = 'первая |вторая |первой |второй |первую |вторую '
HALF = 'половина |половине |половину |пол|пол '

HOURS_1 = '([0-9]|0[0-9]|1[0-2])'
HOURS_2 = '(1[3-9]|2[0-3])'

MINUTES = '(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])'

MIDNIGHT = 'полночь|полуночи'
MIDDAY = 'полдень|полудня'

WITHOUT = 'без ([1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])( минут| минуты| мин)? ([0-9]|0[0-9]|1[0-9]|2[0-3])'

PATH_TO_TIME = 'ner/timeRecognizer/time.csv'


def getWrittenTimeRegexp(case, tens, morning, words):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')
    hours_case, minutes_case = 'hours_' + case, 'minutes_' + case
    minutes_result = ''
    hours_result = ''
    # 20, 30, 40, 50 идут отдельно для точности
    minutes_range = range(56) if not tens else range(56, 60)
    for minute_i in minutes_range:
        minute = dt[minutes_case][minute_i]
        # Сохраняем в словарь, чтоб потом парсить
        words[minute] = int(dt['number'][minute_i])
        # Приписываем 'ноль', потому что в двадцать пять (20:05) никто не говорит
        if minute_i < 10:
            minute = 'ноль ' + minute
        # Сохраняем в регулярку
        if minute_i == 0 or minute_i == 56:
            minutes_result = minute
        else:
            minutes_result = minutes_result + '|' + minute
    # Идем по часам с 0 до 12 если утро, с 13 до 23 иначе
    hours_range = range(13) if morning else range(13, 24)
    for hour_i in hours_range:
        hour = dt[hours_case][hour_i]
        if hour_i == 1:
            words[hour] = int(dt['number'][hour_i])
        # Сохраняем в регулярку
        if hour_i == 0 or hour_i == 13:
            hours_result = hour
        else:
            hours_result = hours_result + '|' + hour
    return '\\b(' + hours_result + ')' + ' ' + '(' + minutes_result + ')\\b'


def getWrittenHourRegexp(case, morning):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')
    case = 'hours_' + case
    result = ''
    # Идем по часам с 0 до 12 если утро, с 13 до 23 иначе
    hours_range = range(13) if morning else range(13, 24)
    for hour_i in hours_range:
        hour = dt[case][hour_i]
        # Сохраняем в регулярку
        if hour_i == 0 or hour_i == 13:
            result = hour
        else:
            result = result + '|' + hour
    return '\\b(' + result + ')( часов| часа| часам)?\\b'


def getInTheMorning(timeRegexp):
    return '\\b(' + timeRegexp + ') утра\\b'


def getInTheDay(timeRegexp):
    return '\\b(' + timeRegexp + ') дня\\b'


def getInTheEvening(timeRegexp):
    return '\\b(' + timeRegexp + ') вечера\\b'


def getInTheNight(timeRegexp):
    return '\\b(' + timeRegexp + ') ночи\\b'

# Половина чего-то


def getHalfRegexp(words):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')
    result = ''
    for i in range(12):
        hour = dt['half'][i]
        # Сохраняем в словарь, чтоб потом парсить
        words[hour] = int(dt['number'][i])
        # Сохраняем в регулярку
        if i == 0:
            result = hour
        else:
            result = result + '|' + hour
    return '\\b(' + WHICH_HALF + ')?(' + HALF + ')(' + result + '|([1-9]|1[0-2]))\\b'


def getWithout(words, morning, h_written, m_written, tens):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')

    minutes_result = '(четверти' if m_written else '([1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])'
    hours_result = '(' if h_written else (HOURS_1 if morning else HOURS_2)

    # 20, 30, 40, 50 идут отдельно для точности
    minutes_range = range(56) if not tens else range(56, 60)
    if m_written:
        minutes_case = 'minutes_without'
        words['четверти'] = 15
        for minute_i in minutes_range:
            minute = dt[minutes_case][minute_i]
            if pd.isna(minute):
                continue
            # Сохраняем в словарь, чтоб потом парсить
            words[minute] = int(dt['number'][minute_i])
            # Сохраняем в регулярку
            minutes_result = minutes_result + '|' + minute
        minutes_result = minutes_result + ')'

    # Идем по часам с 0 до 12 если утро, с 13 до 23 иначе
    hours_range = range(13) if morning else range(13, 24)
    if h_written:
        hours_case = 'hours_im'
        for hour_i in hours_range:
            hour = dt[hours_case][hour_i]
            if hour_i == 1:
                words[hour] = int(dt['number'][hour_i])
            # Сохраняем в регулярку
            if hour_i == 0 or hour_i == 13:
                hours_result = hours_result + hour
            else:
                hours_result = hours_result + '|' + hour
        hours_result = hours_result + ')'

    return '\\bбез ' + minutes_result + '( минут| минуты| мин)? ' + hours_result + '\\b'


def getHoursMinutes(words, morning, h_written, m_written, tens, case):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')

    minutes_result = '(' if m_written else '([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])'
    hours_result = '(' if h_written else (HOURS_1 if morning else HOURS_2)

    # 20, 30, 40, 50 идут отдельно для точности
    minutes_range = range(56) if not tens else range(56, 60)
    if m_written:
        minutes_case = 'minutes_' + case
        for minute_i in minutes_range:
            minute = dt[minutes_case][minute_i]
            # Сохраняем в словарь, чтоб потом парсить
            words[minute] = int(dt['number'][minute_i])
            # Сохраняем в регулярку
            if minute_i == 0 or minute_i == 56:
                minutes_result = minutes_result + minute
            else:
                minutes_result = minutes_result + '|' + minute
        minutes_result = minutes_result + ')'

    # Идем по часам с 0 до 12 если утро, с 13 до 23 иначе
    hours_range = range(13) if morning else range(13, 24)
    if h_written:
        hours_case = 'hours_' + case
        for hour_i in hours_range:
            hour = dt[hours_case][hour_i]
            if hour_i == 1:
                words[hour] = int(dt['number'][hour_i])
            # Сохраняем в регулярку
            if hour_i == 0 or hour_i == 13:
                hours_result = hours_result + hour
            else:
                hours_result = hours_result + '|' + hour
        hours_result = hours_result + ')'

    return '\\b' + hours_result + ' (часов|час|часам|часу|часа) ' + minutes_result + ' (минут|минуту|минутам|минуте|минуты)\\b'

def getHoursOnly(words, morning, h_written, case):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')
    hours_result = '(' if h_written else (HOURS_1 if morning else HOURS_2)

    # Идем по часам с 0 до 12 если утро, с 13 до 23 иначе
    hours_range = range(13) if morning else range(13, 24)
    if h_written:
        hours_case = 'hours_' + case
        for hour_i in hours_range:
            hour = dt[hours_case][hour_i]
            if hour_i == 1:
                words[hour] = int(dt['number'][hour_i])
            # Сохраняем в регулярку
            if hour_i == 0 or hour_i == 13:
                hours_result = hours_result + hour
            else:
                hours_result = hours_result + '|' + hour
        hours_result = hours_result + ')'

    return '\\b' + hours_result + ' (часов|час|часам|часу|часа)\\b'


def getMinutesOf(words, morning, h_written, m_written, tens, case):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')

    minutes_result = '(' if m_written else '([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])'
    hours_result = '(' if h_written else (HOURS_1 if morning else HOURS_2)

    # 20, 30, 40, 50 идут отдельно для точности
    minutes_range = range(56) if not tens else range(56, 60)
    if m_written:
        minutes_case = 'minutes_' + case
        for minute_i in minutes_range:
            minute = dt[minutes_case][minute_i]
            # Сохраняем в словарь, чтоб потом парсить
            words[minute] = int(dt['number'][minute_i])
            # Сохраняем в регулярку
            if minute_i == 0 or minute_i == 56:
                minutes_result = minutes_result + minute
            else:
                minutes_result = minutes_result + '|' + minute
        minutes_result = minutes_result + ')'

    if h_written:
        for hour_i in range(12):
            hour = dt['half'][hour_i]
            if hour_i == 1:
                words[hour] = int(dt['number'][hour_i])
            # Сохраняем в регулярку
            if hour_i == 0 or hour_i == 13:
                hours_result = hours_result + hour
            else:
                hours_result = hours_result + '|' + hour
        hours_result = hours_result + ')'

    nMinutesOfRegexp = '(' + minutes_result + ' (минут|минута|минутам|минуте|минуты|мин))'
    minutesNOfRegexp = '((минут|минута|минутам|минуте|минуты|мин) ' + minutes_result + ')'
    return '\\b(' + nMinutesOfRegexp + '|' + minutesNOfRegexp + ') ' + hours_result + '\\b'


def getAtHour(words, morning, h_written, case):
    dt = pd.read_csv(PATH_TO_TIME, sep=';')

    hours_result = '(' if h_written else (HOURS_1 if morning else HOURS_2)

    if h_written:
        hours_case = 'hours_' + case
        for hour_i in range(12):
            hour = dt[hours_case][hour_i]
            if hour_i == 1:
                words[hour] = int(dt['number'][hour_i])
            # Сохраняем в регулярку
            if hour_i == 0 or hour_i == 13:
                hours_result = hours_result + hour
            else:
                hours_result = hours_result + '|' + hour
        hours_result = hours_result + ')'

    return '\\b(в |к |около )' + hours_result + '( часов| часам| часу| часа| час)?\\b'
