import json
import datetime
import time
import pyfttt
from random import randint

class PointAlerter(object):

    def __init__(self, config, secure_config):
        self.config = config
        self.secure_config = secure_config

    def send_alert(self, current_time):
        pyfttt.send_event(self.secure_config['secret'], self.secure_config['hash'], current_time)
        print "FIRED ALERT: %s" % (current_time)

    def in_play(self, current_datetime):
        current_date = current_datetime.strftime("%d/%m/%Y")
        current_time = current_datetime.strftime("%H:%M")
        day_of_week = current_datetime.weekday()

        if current_date not in self.config["ignore-dates"] and day_of_week in self.config["active-days"]:
            if current_time >= self.config["start-time"] and current_time <= self.config["end-time"]:
                return True

        return False

    def calculate_sleep_to_next_hour_or_start(self, current_datetime):
        current_time = current_datetime.strftime("%H:%M").split(":")
        start_time = self.config["start-time"].split(":")

        if int(current_time[0]) == int(start_time[0]):
            mins_to_start = int(start_time[1]) - int(current_time[1])
            if mins_to_start > 0:
                return mins_to_start
            else:
                return 0
        else:
            return 60 - int(current_time[1])

    def calculate_decision_sleep(self):
        return randint(1, self.config["max-delay-minutes"]) * 60

    def run(self):
            while(True):
                current_datetime = datetime.datetime.now()
                print "ALIVE: %s " % (current_datetime)
                if self.in_play(current_datetime):
                    delay = self.calculate_decision_sleep()
                    time.sleep(delay)
                    updated_datetime = datetime.datetime.now()
                    if self.in_play(updated_datetime):
                        if (randint(0,1) == 1):
                            self.send_alert(updated_datetime.strftime("%d/%m/%Y %H:%M"))
                else:
                    delay = self.calculate_sleep_to_next_hour_or_start(current_datetime) * 60
                    print "Out of play - sleeping for %d seconds" % (delay)
                    time.sleep(delay)

if __name__ == "__main__":
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

    with open('config/secure-config.json', 'r') as secure_config_file:
        secure_config = json.load(secure_config_file)

    PointAlerter(config, secure_config).run()
