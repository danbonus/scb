from datetime import datetime, date, timedelta, time


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
            day = datetime.strptime(self.storage["emulation_date"], "%d.%m.%Y").replace(hour=11)
        if custom_date:
            day = custom_date
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
            #weekday = datetime.strptime(custom_date, "%d.%m.%y")
            weekday = custom_date
        else:
            weekday = self.get_today()
        return weekday.weekday()

    def get_days_of_school(self, custom_date=None):
        weekday = self.get_weekday(custom_date)
        print("День недели: %s" % weekday)
        today = self.get_today(custom_date)
        print("Today: %s" % today.date())
        hour = today.hour

        day_before_yesterday = datetime.date(today - timedelta(days=2))
        yesterday = datetime.date(today - timedelta(days=1))
        print("Yesterday: %s" % yesterday)
        last_day = datetime.date(today)  # today

        next_day = datetime.date(today + timedelta(days=1))  # tomorrow
        day_after_tomorrow = datetime.date(today + timedelta(days=2))

        if weekday == 5:  # Суббота
            next_day = day_after_tomorrow
        elif weekday == 6:  # Воскресенье
            return yesterday, next_day  # не учимся, следующая проверка не нужна

        if hour < 8:  # если учебный день еще не начался
            if weekday == 0:  # если сейчас понедельник, то предыдущий учебный день -- позавчера, суббота
                next_day = last_day  # след. день -- понедельник
                last_day = day_before_yesterday
            else:
                next_day = last_day
                last_day = yesterday

        print(last_day)
        print(next_day)
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

    def time_of_day(self, in_time=None):
        now = datetime.now()

        if not in_time:
            hour = now.hour
        else:
            hour = in_time.hour

        if hour < 5:
            return self.night
        elif hour < 11:
            return self.morning
        elif hour < 17:
            return self.afternoon
        elif hour < 23:
            return self.evening
        elif hour == 23:
            return self.night

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

    @staticmethod
    def now():
        return datetime.now()

    def hm_format(self, message):
        datetime.strptime(message, '%H:%M')
