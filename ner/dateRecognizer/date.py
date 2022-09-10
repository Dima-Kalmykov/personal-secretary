#!/usr/bin/env python
# encoding: utf-8
"""
date.py
"""

from datetime import datetime, timedelta
import re
import ner.dateRecognizer.dateparsers as dp
import ner.dateRecognizer.dateregexp as dr


def findDate(text, sendingDate, regexps, parsers):
    for i in range(len(regexps)):
        regexp, parser = regexps[i], parsers[i]
        match = re.search(regexp, text,  flags=re.IGNORECASE)
        if match:
            match = match[0]
            return parser(match, sendingDate)
    return sendingDate + timedelta(days=1)


def getDateRecognizer():
    dict = {}
    regexps = dr.getAllRegexps(dict)
    parsers = dp.getAllParsers(dict)

    return lambda text, sendingDate: findDate(text, sendingDate, regexps, parsers)
