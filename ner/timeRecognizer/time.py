#!/usr/bin/env python
# encoding: utf-8
"""
time.py
"""

from datetime import timedelta
import re
import ner.timeRecognizer.timeparsers as tp
import ner.timeRecognizer.timeregexp as tr

def findTime(text, regexps, parsers):
    for i in range(len(regexps)):
        regexp, parser = regexps[i], parsers[i]
        match = re.search(regexp, text,  flags=re.IGNORECASE)
        if match:
            match = match[0]
            return parser(match)
    return timedelta(hours=9)


def getTimeRecognizer():
    words = {}
    regexps = tr.getAllRegexps(words)
    parsers = tp.getAllParsers(words)
    return lambda text: findTime(text, regexps, parsers)
