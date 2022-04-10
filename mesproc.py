import re
from datetime import date, timedelta
from datetime import datetime as dt

import spacy
import translators as ts


class EventProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.t = ts.google

    def extract_datetime(self, text_date="", text_time="9:00"):
        if text_time == '':
            text_time = "9:00"
        if text_date == "":
            daystamp = date.today()
        elif text_date.lower().find("after tomorrow") != -1:
            daystamp = date.today() + timedelta(days=2)
        elif text_date.lower().find("tomorrow") != -1:
            daystamp = date.today() + timedelta(days=1)
        elif text_date.lower().find("week") != -1:
            daystamp = date.today() + timedelta(weeks=1)
        else:
            day = re.search(r'\d{1,2}', text_date).group()
            month = re.search(r'[A-Za-z]{1,10}', text_date).group()
            year = str(date.today().year)
            daystamp = dt.strptime(' '.join([day, month, year]), "%d %B %Y")
        timestamp = dt.strptime(text_time, "%H:%M").time()
        return dt.combine(daystamp, timestamp)

    def extract_summary(self, msg=""):
        preps = [' at ', ' with ', ' on ', ' in ']
        for prep in preps:
            msg = msg.replace(prep, '')
        msg = self.t(msg, to_language='ru')
        return msg.lower()

    def process_message(self, msg=""):
        translated_msg = self.t(msg, from_language='ru')
        doc = self.nlp(translated_msg)
        text_time = ""
        text_date = ""
        pers = ""
        loc = ""
        summary = doc.text
        for ent in doc.ents:
            if ent.label_ == 'TIME':
                text_time = str(ent)
            if ent.label_ == 'DATE':
                text_date = str(ent)
            if ent.label_ == 'PERSON':
                pers = self.t(str(ent), to_language='ru')
            if ent.label_ == 'LOC' or ent.label_ == 'ORG' or ent.label_ == 'GPE':
                loc = self.t(str(ent), to_language='ru')
            summary = summary.replace(str(ent), '')
        timestamp = self.extract_datetime(text_date, text_time)
        if pers != "" and loc != "":
            summary = f"{pers}: {self.extract_summary(summary)}, {loc}"
        elif pers != "":
            summary = f"{pers}: {self.extract_summary(summary)}"
        elif loc != "":
            summary = f"{loc}: {self.extract_summary(summary)}"
        else:
            summary = f"{self.extract_summary(summary)}"
        return summary, timestamp


result = EventProcessor().process_message("Встреча с Машей в 9:00")

print(result)
