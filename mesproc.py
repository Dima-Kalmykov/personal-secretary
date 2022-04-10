import spacy
import translators as ts
from datetime import datetime as dt
from datetime import date, time, timedelta

class EventProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.t = ts.google

    def extract_datetime(text_date="", text_time=""):
        daystamp = date.today()
        timestamp = time(12, 0, 0)
        if text_date.lower().find("after tomorrow") != -1:
            daystamp = date.today() + timedelta(days=2)
        elif text_date.lower().find("tomorrow") != -1:
            daystamp = date.today() + timedelta(days=1)
        elif text_date.lower().find("week") != -1:
            daystamp = date.today() + timedelta(weeks=1)
        else:
            day = re.search(r'\d{1,2}', text_date).group()
            month = re.search(r'[A-Za-z]{1,10}', s).group()
            year = str(date.today().year)
            daystamp = dt.strptime(' '.join([day, month, year]), "%d %B %Y")
        timestamp = dt.strptime(text_time, "%H:%M").time()
        return dt.combine(daystamp, timestamp)

    def extract_summary(msg=""):
        preps = [' at ', ' with ', ' on ', ' in ']
        for prep in preps:
            msg = msg.replace(prep, '')
        msg = t(msg, to_language='ru')
        return msg.lower()

    def process_message(msg=""):
        translated_msg = t(msg, from_language='ru')
        doc = nlp(translated_msg)
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
                pers = str(ent)
            if ent.label_ == 'LOC' or ent.label_ == 'ORG' or  ent.label_ == 'GPE':
                loc = str(ent)
            summary = summary.replace(str(ent), '')
        timestamp = extract_datetime(text_date, text_time)
        if pers != "" and loc != "":
            summary = f"{pers}: {extract_summary(summary)}, {loc}"
        elif pers != "":
            summary = f"{pers}: {extract_summary(summary)}"
        elif loc != "":
            summary = f"{loc}: {extract_summary(summary)}"
        else:
            summary = f"{extract_summary(summary)}"
        return summary, timestamp
