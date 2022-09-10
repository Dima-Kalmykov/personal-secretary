#!/usr/bin/env python
# encoding: utf-8
"""
persons.py
"""

import spacy


def findPersons(text, model):
    doc = model(text)
    persons = [x for x in doc.ents if x.label_ == 'PER']
    return [x.lemma_.title() for x in persons]


def getPersonsRecognizer():
    model = spacy.load("ru_core_news_lg")
    return lambda text: findPersons(text, model)
