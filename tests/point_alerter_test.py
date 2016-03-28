import unittest
import datetime
from app.point_alerter import PointAlerter

class PointAlertTest(unittest.TestCase):

    START_TIME = "10:10"
    END_TIME = "16:00"
    ACTIVE_TIME = "12:00"
    BEFORE_START = "09:00"
    AFTER_END = "18:00"

    ACTIVE_DAY = "11/10/2016"
    INACTIVE_DAY = "09/10/2016"
    IGNORE_DAY = "10/10/2016"

    INACTIVE_DAY_ACTIVE_TIME = "%s %s" % (INACTIVE_DAY, ACTIVE_TIME)
    IGNORE_DAY_ACTIVE_TIME = "%s %s" % (IGNORE_DAY, ACTIVE_TIME)
    ACTIVE_DAY_BEFORE_START = "%s %s" % (ACTIVE_DAY, BEFORE_START)
    ACTIVE_DAY_AFTER_END = "%s %s" % (ACTIVE_DAY, AFTER_END)
    ACTIVE_DAY_ACTIVE_TIME = "%s %s" % (ACTIVE_DAY, ACTIVE_TIME)
    ACTIVE_DAY_START_TIME = "%s %s" % (ACTIVE_DAY, START_TIME)
    ACTIVE_DAY_END_TIME = "%s %s" % (ACTIVE_DAY, END_TIME)

    def setUp(self):
        config = {
            "start-time":self.START_TIME,
            "end-time":self.END_TIME,
            "active-days": [0,1],
            "ignore-dates": self.IGNORE_DAY
        }

        secure_config = {}

        self.alerter = PointAlerter(config, secure_config)

    def test_in_play_inactive_day_returns_False(self):
        current = self.create_datetime(self.INACTIVE_DAY_ACTIVE_TIME)
        result = self.alerter.in_play(current)
        self.assertFalse(result)

    def test_in_play_ignore_date_returns_False(self):
        current = self.create_datetime(self.IGNORE_DAY_ACTIVE_TIME)
        result = self.alerter.in_play(current)
        self.assertFalse(result)

    def test_in_play_too_early_returns_False(self):
        current = self.create_datetime(self.ACTIVE_DAY_BEFORE_START)
        result = self.alerter.in_play(current)
        self.assertFalse(result)

    def test_in_play_too_late_returns_False(self):
        current = self.create_datetime(self.ACTIVE_DAY_AFTER_END)
        result = self.alerter.in_play(current)
        self.assertFalse(result)

    def test_in_play_active_day_time_returns_True(self):
        current = self.create_datetime(self.ACTIVE_DAY_ACTIVE_TIME)
        result = self.alerter.in_play(current)
        self.assertTrue(result)

    def test_in_play_start_time_returns_True(self):
        current = self.create_datetime(self.ACTIVE_DAY_START_TIME)
        result = self.alerter.in_play(current)
        self.assertTrue(result)

    def test_in_play_end_time_returns_True(self):
        current = self.create_datetime(self.ACTIVE_DAY_END_TIME)
        result = self.alerter.in_play(current)
        self.assertTrue(result)

    def test_sleep_calculation_full_hour(self):
        current = self.create_datetime(self.ACTIVE_DAY_BEFORE_START)
        result = self.alerter.calculate_sleep_to_next_hour_or_start(current)
        self.assertEquals(60, result)

    def test_sleep_calculation_minutes_to_start(self):
        current = self.create_datetime("%s 10:07" % self.ACTIVE_DAY)
        result = self.alerter.calculate_sleep_to_next_hour_or_start(current)
        self.assertEquals(3, result)

    def test_sleep_calculation_minutes_to_next_hour(self):
        current = self.create_datetime("%s 09:45" % self.ACTIVE_DAY)
        result = self.alerter.calculate_sleep_to_next_hour_or_start(current)
        self.assertEquals(15, result)

    def test_sleep_calculation_minutes_to_next_hour_on_hour(self):
        current = self.create_datetime("%s 09:00" % self.ACTIVE_DAY)
        result = self.alerter.calculate_sleep_to_next_hour_or_start(current)
        self.assertEquals(60, result)

    def test_sleep_calculation_minutes_in_start_hour(self):
        current = self.create_datetime("%s 10:15" % self.ACTIVE_DAY)
        result = self.alerter.calculate_sleep_to_next_hour_or_start(current)
        self.assertEquals(0, result)

    def test_sleep_calculation_minutes_on_start_time(self):
        current = self.create_datetime(self.ACTIVE_DAY_START_TIME)
        result = self.alerter.calculate_sleep_to_next_hour_or_start(current)
        self.assertEquals(0, result)

    def create_datetime(self, date_string):
        return datetime.datetime.strptime(date_string, "%d/%m/%Y %H:%M")
