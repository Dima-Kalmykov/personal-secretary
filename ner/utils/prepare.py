#!/usr/bin/env python
# encoding: utf-8
"""
prepare.py
"""

import re


def prepareText(text):
    text = re.sub('\s+', ' ', text)
    return re.sub('(, |\. )', ' ', text)
