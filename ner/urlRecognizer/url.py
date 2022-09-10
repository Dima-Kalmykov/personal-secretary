#!/usr/bin/env python
# encoding: utf-8
"""
url.py
"""

import re


PATH_TO_REGEXP = 'ner/urlRecognizer/regexp.txt'


def findUrl(text, regexp):
    match = re.search(regexp, text,  flags=re.IGNORECASE)
    return match[0] if match else None


def getUrlRecognizer():
    with open(PATH_TO_REGEXP) as f:
        regexp = f.readlines()[0]

    return lambda text: findUrl(text, regexp)
