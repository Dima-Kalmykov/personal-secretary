from calendar import monthrange
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import unittest

import os
import sys

p = os.path.abspath('.')
sys.path.insert(1, p)

from ner.dateRecognizer.date import getDateRecognizer


def getCurrentDate():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


def getNearestWeekends(today):
    return today + timedelta(weeks=1 if today.isoweekday() > 5 else 0, days=6-today.isoweekday())


class TestTimeRecognizer(unittest.TestCase):
    def __init__(self, name):
        self.recognizer = getDateRecognizer()
        unittest.TestCase.__init__(self, name)

    def testStandartNormal(self):
        for m in range(1, 13):
            maxDay = monthrange(2024, m)[1]
            for d in range(1, maxDay + 1, 5):
                for sep in ['.', '/', '-', ' ']:
                    test = 'встреть меня ' + \
                        str(d).zfill(2) + sep + \
                        str(m).zfill(2) + sep + '2024 в парке'
                    self.assertEqual(
                        self.recognizer(test, getCurrentDate()),
                        datetime(year=2024, month=m, day=d)
                    )

    def testStandartIncorrectDay(self):
        for m in range(1, 13):
            maxDay = monthrange(2024, m)[1]
            for d in range(maxDay + 1, 32, 1):
                for sep in ['.', '/', '-', ' ']:
                    test = 'встреть меня ' + \
                        str(d).zfill(2) + sep + str(m).zfill(2) + \
                        sep + '2024' + ' в парке'
                    expected = {
                        'year': 2024 if m < 12 else 2024,
                        'month': m + 1 if m < 12 else 1,
                        'day': d - maxDay
                    }
                    self.assertEqual(
                        self.recognizer(test, getCurrentDate()),
                        datetime(
                            year=expected['year'], month=expected['month'], day=expected['day'])
                    )

    def testStandartAutoYear(self):
        for m in range(1, 13):
            maxDay = monthrange(2024, m)[1]
            for d in range(1, maxDay + 1, 5):
                for sep in ['.', '/', '-', ' ']:
                    test = 'встреть меня ' + \
                        str(d).zfill(2) + sep + \
                        str(m).zfill(2) + sep + ' в парке'
                    self.assertEqual(
                        self.recognizer(test, getCurrentDate()),
                        datetime(year=getCurrentDate().year, month=m, day=d)
                    )

    def testWrittenMonthParser(self):
        test = 'встреть меня 24 сентября 2033.'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=2033, month=9, day=24)
        )

    def testWrittenMonthParserOverflow(self):
        test = 'встреть меня 31 сентября 2033.'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=2033, month=10, day=1)
        )

    def testWrittenMonthParserAutoYear(self):
        test = 'встреть меня 1 июня в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=getCurrentDate().year, month=6, day=1)
        )

    def testWrittenDayMonthParser(self):
        test = 'встреть меня пятого сентября 2033'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=2033, month=9, day=5)
        )

    def testWrittenMonthParserOverflow(self):
        test = 'встреть меня тридцать первого сентября 2025'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=2025, month=10, day=1)
        )

    def testWrittenMonthParserAutoYear(self):
        test = 'встреть меня первого июня в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=getCurrentDate().year, month=6, day=1)
        )

    def testToday(self):
        test = 'встреть меня сегодня в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate()
        )

    def testTomorrow(self):
        test = 'встреть меня завтра в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(days=1)
        )

    def testTheDayAfterTomorrow1(self):
        test = 'встреть меня послезавтра в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(days=2)
        )
    
    def testTheDayAfterTomorrow2(self):
        test = 'встреть меня после завтра в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(days=2)
        )

    def testWeekends1(self):
        test = 'встретимся на выходных в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getNearestWeekends(getCurrentDate())
        )

    def testWeekends2(self):
        test = 'встретимся на выхах в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getNearestWeekends(getCurrentDate())
        )

    def testWeekends3(self):
        test = 'встретимся в выходные в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getNearestWeekends(getCurrentDate())
        )

    def testWeekends4(self):
        test = 'встретимся в выхи в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getNearestWeekends(getCurrentDate())
        )

    def testNextWeek1(self):
        test = 'встретимся на следующей неделе в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            today + timedelta(days=8-today.isoweekday())
        )

    def testNextWeek2(self):
        test = 'встретимся на след неделе в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            today + timedelta(days=8-today.isoweekday())
        )

    def testNextWeek3(self):
        test = 'встретимся на некст неделе в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            today + timedelta(days=8-today.isoweekday())
        )

    def testNextWeek4(self):
        test = 'встретимся на некст неделе в пятницу в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            today + timedelta(days=8-today.isoweekday()+4)
        )

    def testNextWeek5(self):
        test = 'встретимся в среду на следущей неделе в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            today + timedelta(days=8-today.isoweekday()+2)
        )

    def testNextMonth(self):
        test = 'встретимся в следущем месяце в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            today + timedelta(days=monthrange(today.year,
                              today.month)[1]-today.day+1)
        )

    def testDayOfTheWeek1(self):
        weekdays = {
            'понедельник': 1,
            'вторник': 2,
            'среда': 3,
            'четверг': 4,
            'пятница': 5,
            'суббота': 6,
            'воскресенье': 7,
            'пн': 1,
            'вт': 2,
            'ср': 3,
            'чт': 4,
            'пт': 5,
            'сб': 6,
            'вс': 7,
        }
        for day in weekdays:
            test = 'встретимся в ' + day + ' в парке'
            today = getCurrentDate()
            weekday = today.isoweekday()
            day = weekdays[day]
            self.assertEqual(
                self.recognizer(test, getCurrentDate()),
                today + timedelta(days=day-weekday if weekday <
                                  day else day-weekday+7)
            )

    def testInDays1(self):
        test = 'встретимся через 3 дня в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(days=3)
        )

    def testInDays2(self):
        test = 'встретимся через день в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(days=1)
        )

    def testInDays3(self):
        test = 'встретимся через два дня в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(days=2)
        )

    def testInWeeks1(self):
        test = 'встретимся через 4 недели в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(weeks=4)
        )

    def testInWeeks2(self):
        test = 'встретимся через неделю в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(weeks=1)
        )

    def testInWeeks3(self):
        test = 'встретимся через пять недели в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + timedelta(weeks=5)
        )

    def testInMonths1(self):
        test = 'встретимся через 4 месяца в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + relativedelta(months=4)
        )

    def testInMonths2(self):
        test = 'встретимся через месяц в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + relativedelta(months=1)
        )

    def testInMonths3(self):
        test = 'встретимся через пять месяцев в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + relativedelta(months=5)
        )

    def testInYear1(self):
        test = 'встретимся через 4 года в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + relativedelta(years=4)
        )

    def testInYear2(self):
        test = 'встретимся через год в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + relativedelta(years=1)
        )

    def testInYear3(self):
        test = 'встретимся через пять лет в парке'
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            getCurrentDate() + relativedelta(years=5)
        )
    
    def testMonth(self):
        test = 'встретимся в мае в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=today.year if today.month <= 5 else today.year+1, month=5, day=1)
        )
    
    def testNumbersOfMonth1(self):
        test = 'встретимся в 20х числах апреля в парке'
        today = getCurrentDate()
        y = today.year if today.month <= 4 else today.year+1
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=y, month=4, day=20)
        )
    
    def testNumbersOfMonth2(self):
        test = 'встретимся в первых числах декабря в парке'
        today = getCurrentDate()
        y = today.year if today.month <= 12 else today.year+1
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=y, month=12, day=1)
        )
    
    def testNumbersOfMonth3(self):
        test = 'встретимся в первых числах сентября в парке'
        today = getCurrentDate()
        y = today.year if today.month <= 9 else today.year+1
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=y, month=9, day=1)
        )
    
    def testNumbersOfMonth4(self):
        test = 'встретимся в 10 числах этого месяца в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=today.year, month=today.month, day=10)
        )
    
    def testNumbersOfMonth5(self):
        test = 'встретимся в 30 числах некст месяца в парке'
        today = getCurrentDate()
        y = today.year if today.month+1 <= 12 else today.year+1
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=y, month=today.month+1, day=30)
        )
    
    def testNumbersOfMonth6(self):
        test = 'встретимся в 10 числах месяца в парке'
        today = getCurrentDate()
        self.assertEqual(
            self.recognizer(test, getCurrentDate()),
            datetime(year=today.year, month=today.month, day=10)
        )


if __name__ == '__main__':
    unittest.main()
