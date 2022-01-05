from datetime import datetime, date, timedelta, time

from logger import logger


class TimeRepository:
    def __init__(self, storage):
        self.storage = storage
        self.night = "night"
        self.morning = "morning"
        self.afternoon = "afternoon"
        self.evening = "evening"

    def get_hour(self):
        pass

    def get_today(self, custom_date=None):
        day = datetime.today()
        if 'emulation_date' in self.storage:
            day = self.storage["emulation_date"]
        if custom_date:
            day = custom_date.replace(hour=11)
        return day

    def get_tomorrow(self, custom_date=None):
        day_from = self.get_today()
        if custom_date:
            day_from = datetime.strptime(custom_date, "%d.%m.%Y")
        return day_from + timedelta(days=1)

    def get_yesterday(self, custom_date=None):
        day_from = self.get_today()
        if custom_date:
            day_from = datetime.strptime(custom_date, "%d.%m.%Y")
        return day_from - timedelta(days=1)

    def get_timestamp(self):
        today = self.get_today()
        return int(today.timestamp())

    def get_time_of_day(self):
        pass

    def get_weekday(self, custom_date=None):
        if custom_date:
            day = custom_date
        else:
            day = self.get_today()
        return day.weekday()

    def get_date_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp)

    def get_days_of_school(self, custom_date=None):
        weekday = self.get_weekday(custom_date)
        #print("День недели: %s" % weekday)
        today = self.get_today(custom_date)
        #print("Today: %s" % today.date())
        hour = today.hour
        #print("Hour: %s" % hour)

        today = datetime.combine(self.get_today(custom_date), time.min)

        day_before_yesterday = today - timedelta(days=2)
        yesterday = today - timedelta(days=1)
        #print("Yesterday: %s" % yesterday)
        last_day = today  # today

        next_day = today + timedelta(days=1)  # tomorrow
        day_after_tomorrow = today + timedelta(days=2)

        if weekday == 5:  # Суббота
            next_day = day_after_tomorrow
        elif weekday == 6:  # Воскресенье
            return yesterday, next_day  # не учимся, следующая проверка не нужна

        if hour < 8:  # если учебный день еще не начался
            logger.debug('день не начался')
            if weekday == 0:  # если сейчас понедельник, то предыдущий учебный день -- позавчера, суббота
                next_day = last_day  # след. день -- понедельник
                last_day = day_before_yesterday
            else:
                next_day = last_day
                last_day = yesterday

        return last_day, next_day

    def is_today(self, timestamp):
        given_date = date.fromtimestamp(timestamp)
        today_date = self.get_today().date()
        return given_date == today_date

    def get_day_time_borders(self, custom_date=None):
        midnight = datetime.combine(self.get_today() if not custom_date else custom_date, time.min)  #
        start = int(midnight.timestamp())
        end = start + 111600
        return start, end

    def get_start_timestamp(self, timestamp):
        return int(datetime.combine(datetime.fromtimestamp(timestamp), time.min).timestamp())

    def time_of_day(self, custom_time=None):
        now = datetime.now()

        if not custom_time:
            hour = now.hour
        else:
            hour = custom_time.hour

        if hour < 5 or hour == 23:
            return self.night
        elif hour < 11:
            return self.morning
        elif hour < 17:
            return self.afternoon
        elif hour < 23:
            return self.evening

    def str_to_timestamp(self, date=''):
        time1 = None
        if not date:
            time = datetime.now()
        elif len(date.split("-")) == 1:
            time = datetime.strptime(date, "%d.%m.%y")
        elif len(date.split("-")) == 2:
            time = datetime.strptime(date.split("-")[0], "%d.%m.%y")
            time1 = datetime.strptime(date.split("-")[1], "%d.%m.%y")
        else:
            return False
        timestamp = int(time.timestamp())
        return timestamp, int(time1.timestamp()) + 83699 if time1 else int(timestamp) + 83699

    def timestamp_from_date(self, string_date):
        date_object = datetime.strptime(string_date, "%d.%m.%Y")
        return date_object.timestamp()

    @staticmethod
    def now():
        return datetime.now()

    def hm_format(self, message):
        datetime.strptime(message, '%H:%M')
