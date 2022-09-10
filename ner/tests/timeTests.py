from datetime import timedelta
import unittest

import os
import sys

p = os.path.abspath('.')
sys.path.insert(1, p)

from ner.timeRecognizer.time import getTimeRecognizer

class TestTimeRecognizer(unittest.TestCase):
    def __init__(self, name):
        self.recognizer = getTimeRecognizer()
        unittest.TestCase.__init__(self, name)

    def testStandart(self):
        for h in range(0, 24, 5):
            for m in range(0, 60, 5):
                for sep in [':', ';', '.', ' ']:
                    test = 'встреть меня в ' + str(h).zfill(2) + sep + str(m).zfill(2) + ' в парке'
                    self.assertEqual(
                        self.recognizer(test),
                        timedelta(hours=h, minutes=m)
                    )
    
    def testStandartMorning(self):
        for h in range(1, 12, 5):
            for m in range(0, 60, 5):
                for sep in [':', ';', '.', ' ']:
                    test = 'встреть меня в ' + str(h).zfill(2) + sep + str(m).zfill(2) + ' утра в парке'
                    self.assertEqual(
                        self.recognizer(test),
                        timedelta(hours=h, minutes=m)
                    )
    
    def testStandartDay(self):
        for h in range(1, 12, 5):
            for m in range(0, 60, 5):
                for sep in [':', ';', '.', ' ']:
                    test = 'встреть меня в ' + str(h).zfill(2) + sep + str(m).zfill(2) + ' дня в парке'
                    self.assertEqual(
                        self.recognizer(test),
                        timedelta(hours=h + 12, minutes=m)
                    )
    
    def testStandartEvening(self):
        for h in range(1, 12, 5):
            for m in range(0, 60, 5):
                for sep in [':', ';', '.', ' ']:
                    test = 'встреть меня в ' + str(h).zfill(2) + sep + str(m).zfill(2) + ' вечера в парке'
                    self.assertEqual(
                        self.recognizer(test),
                        timedelta(hours=h + 12, minutes=m)
                    )
    
    def testStandartNight(self):
        for h in range(1, 12, 5):
            for m in range(0, 60, 5):
                for sep in [':', ';', '.', ' ']:
                    test = 'встреть меня в ' + str(h).zfill(2) + sep + str(m).zfill(2) + ' ночи в парке'
                    self.assertEqual(
                        self.recognizer(test),
                        timedelta(hours=h, minutes=m)
                    )

    def testMidnight(self):
        test = 'встреть меня в полночь в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=0, minutes=0)
        )
    
    def testMidday(self):
        test = 'встреть меня в полдень в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=12, minutes=0)
        )
    
    def testFullyWritten1(self):
        test = 'встреть меня в девять тридцать в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=9, minutes=30)
        )
    
    def testFullyWritten2(self):
        test = 'встреть меня в одиннадцать тридцать пять в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=11, minutes=35)
        )
    
    def testFullyWritten3(self):
        test = 'встреть меня к двадцати двум сорока пяти в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=22, minutes=45)
        )
    
    def testHour1(self):
        test = 'встреть меня часов в семь в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=19, minutes=0)
        )
    
    def testHour2(self):
        test = 'встреть меня к пяти часам в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=17, minutes=0)
        )
    
    def testHourMorning(self):
        test = 'встреть меня в три часа утра в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=3, minutes=0)
        )
    
    def testHourDay(self):
        test = 'встреть меня в час дня в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=13, minutes=0)
        )
    
    def testHourEvening(self):
        test = 'встреть меня в 8 часов вечера в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=20, minutes=0)
        )
    
    def testHourNight(self):
        test = 'встреть меня часа в 2 ночи в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=2, minutes=0)
        )
    
    def testHalf1(self):
        test = 'встреть меня в пол 11 в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=10, minutes=30)
        )
    
    def testHalf2(self):
        test = 'встреть меня в полтретьего в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=14, minutes=30)
        )
    
    def testHalf3(self):
        test = 'встреть меня в пол первого в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=12, minutes=30)
        )
    
    def testHalf4(self):
        test = 'встреть меня к половине третьего в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=14, minutes=30)
        )
    
    def testWithout1(self):
        test = 'встреть меня в без 10 минут 4 в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=15, minutes=50)
        )
    
    def testWithout2(self):
        test = 'встреть меня в без пяти 10 в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=9, minutes=55)
        )
    
    def testWithout3(self):
        test = 'встреть меня в без четверти семь в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=18, minutes=45)
        )
    
    def testWithout4(self):
        test = 'встреть меня в без десяти час в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=12, minutes=50)
        )
    
    def testHoursMinutes1(self):
        test = 'встреть меня в 5 часов 10 минут утра в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=5, minutes=10)
        )
    
    def testHoursMinutes2(self):
        test = 'встреть меня в одиннадцать часов сорок минут в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=11, minutes=40)
        )
    
    def testHoursMinutes3(self):
        test = 'встреть меня к шести часам 11 минутам в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=18, minutes=11)
        )
    
    def testHoursOnly1(self):
        test = 'встреть меня в 5 часов в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=17)
        )
    
    def testHoursOnly2(self):
        test = 'встреть меня в двадцать два часа в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=22)
        )
    
    def testHoursOnlyMorning(self):
        test = 'встреть меня к 3 часам утра в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=3)
        )
    
    def testMinutesOf1(self):
        test = 'встреть меня к 10 минутам первого в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=12, minutes=10)
        )
    
    def testMinutesOf2(self):
        test = 'встреть меня к пяти минутам второго в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=13, minutes=5)
        )
    
    def testMinutesOf3(self):
        test = 'встреть меня к минутам двадцати третьего в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=14, minutes=20)
        )
    
    def testMinutesOf4(self):
        test = 'встреть меня к минутам 7 третьего в парке'
        self.assertEqual(
            self.recognizer(test),
            timedelta(hours=14, minutes=7)
        )

if __name__ == '__main__':
    unittest.main()
