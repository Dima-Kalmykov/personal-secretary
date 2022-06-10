import re
from datetime import date, timedelta, time
from datetime import datetime as dt

import spacy


class EventProcessor:
    def __init__(self):
        self.nlp = None

    def extract_date(self, text_date="", dt_time=time(9, 0, 0)):
        months = {'января' : 'Jan', 'февраля' : 'Feb', 'марта' : 'Mar',
                  'апреля' : 'Apr', 'мая' : 'May', 'июня' : 'Jun',
                  'июля' : 'Jul', 'августа' : 'Aug', 'сентября' : 'Sep',
                  'октября' : 'Oct', 'ноября' : 'Nov', 'декабря' : 'Dec'}
        weekdays = {'понедельник': 0, 'вторник' : 1,
                        'среду' : 2, 'четверг' : 3,
                        'пятницу' : 4, 'субботу' : 5,
                        'воскресенье' : 6}
        if text_date == "":
            daystamp = date.today()
            cur_tm = dt.now() + timedelta(hours=3)
            if str(dt.combine(daystamp, dt_time) - cur_tm)[0] == '-':
                daystamp += timedelta(days=1)
        elif text_date.lower().find("послезавтра") != -1:
            daystamp = date.today() + timedelta(days=2)
        elif text_date.lower().find("завтра") != -1:
            daystamp = date.today() + timedelta(days=1)
        elif text_date.lower().find("сегодня") != -1:
            daystamp = date.today()
        elif text_date.lower() in weekdays:
            daystamp = date.today()
            days_diff = weekdays[text_date] - daystamp.weekday()
            if days_diff < 0:
                days_diff += 7
            daystamp += timedelta(days=days_diff)
        elif len(text_date.split()) == 2:
            day, month = text_date.split()[0], months[text_date.split()[1]]
            year = str(date.today().year)
            daystamp = dt.strptime(' '.join([day, month, year]), "%d %b %Y")
            if daystamp.date() < date.today():
                daystamp += timedelta(days=365)
        else:
            daystamp = date.today() + timedelta(days=1)
        return dt.combine(daystamp, dt_time)

    def extract_time(self, text_time="9:00"):
        if text_time == '':
            return dt.strptime("9:00", "%H:%M").time()
        elif text_time.lower().find(":") != -1:
            try:
                timestamp = dt.strptime(text_time, "%H:%M").time()
                return timestamp
            except Exception as exp:
                timestamp = dt.strptime("9:00", "%H:%M").time()
                return timestamp
        elif 'утра' in text_time:
            hour = int(text_time.split()[0])
            if 3 <= hour and hour <= 12:
                timestamp = time(hour, 0, 0)
            else:
                timestamp = time(9, 0, 0)
            return timestamp
        elif 'вечера' in text_time:
            hour = int(text_time.split()[0])
            if 3 <= hour and hour <= 12:
                timestamp = time((hour + 12) % 24, 0, 0)
            else:
                timestamp = time(18, 0, 0)
            return timestamp


    def extract_datetime(self, text_date="", text_time="9:00"):
        timestamp = self.extract_time(text_time)
        return self.extract_date(text_date, timestamp)

    def extract_summary(self, time_ind, date_ind, msg=""):
        if msg == "":
            return ""
        words = msg.split()
        preps = ['в', 'на', 'с']
        tbr = []
        if time_ind != () and words[time_ind[0] - 1].lower() in preps:
            time_ind = (time_ind[0] - 1, time_ind[1])
        if date_ind != () and words[date_ind[0] - 1].lower() in preps:
            date_ind = (date_ind[0] - 1, date_ind[1])
        final_words = []
        if date_ind != () and time_ind != ():
            if date_ind[0] < time_ind[0]:
                final_words = words[:date_ind[0]] + words[date_ind[1]:time_ind[0]] + words[time_ind[1]:]
            else:
                final_words = words[:time_ind[0]] + words[time_ind[1]:date_ind[0]] + words[date_ind[1]:]
        elif date_ind != ():
            final_words = words[:date_ind[0]] + words[date_ind[1]:]
        elif time_ind != ():
            final_words = words[:time_ind[0]] + words[time_ind[1]:]
        else:
            final_words = words
        return ' '.join([final_words[0].capitalize()] + final_words[1:])

    def process_message(self, msg=""):
        if self.nlp is None:
            self.nlp = spacy.load('./final_output')
        doc = self.nlp(msg)
        text_time = ""
        text_date = ""
        time_flag = False
        date_flag = False
        summary = doc.text
        date_ind, time_ind = (), ()
        for ent in doc.ents:
            if ent.label_ == 'TIME' and not time_flag:
                text_time = str(ent)
                time_flag = True
                time_ind = (ent.start, ent.end)
            if ent.label_ == 'DATE' and not date_flag:
                text_date = str(ent)
                date_flag = True
                date_ind = (ent.start, ent.end)
        timestamp = self.extract_datetime(text_date, text_time)
        summary = self.extract_summary(time_ind, date_ind, summary)
        return summary, timestamp


# result = EventProcessor().process_message("Встреча с Машей в 9:00")

# print(result)
