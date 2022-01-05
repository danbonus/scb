from datetime import datetime, time, timedelta


class MyTime:
    def __init__(self, scb):
        self.night = "night"
        self.morning = "morning"
        self.afternoon = "afternoon"
        self.evening = "evening"
        self.scb = scb

    def get_today(self):
        if 'emulation_date' in self.scb.storage:
            return self.scb.storage["emulation_date"]
        else:
            return datetime.today()

    def get_timestamp(self):
        today = self.get_today()
        return int(today.timestamp())

    def time_of_day(self, in_time=None):
        time = datetime.now()

        if not in_time:
            hour = time.hour
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

    def get_weekday(self, string=''):
        if string:
            weekday = datetime.strptime(string, "%d.%m.%y")
        else:
            weekday = datetime.now()
        return weekday.weekday()

    def check_for_weekday(self):
        weekday = self.get_weekday()
        hour = datetime.now().hour
        today = self.get_today()

        day_before_yesterday = datetime.date(today - timedelta(days=2))
        yesterday = datetime.date(today - timedelta(days=1))

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
                last_day = yesterday
                next_day = last_day

        return last_day, next_day

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

    def check(self, timestamp):  # Check if given timestamp date == today date
        midnight = datetime.combine(self.get_today(), time.min)
        start = int(midnight.timestamp())
        end = start + 83699
        if start < timestamp < end:
            return True

    def start_end(self, date=None):
        midnight = datetime.combine(self.get_today() if not date else date, time.min)
        start = int(midnight.timestamp())
        end = start + 111600
        return start, end

    @property
    def now(self):
        return datetime.now()

    def hm_format(self, message):
        datetime.strptime(message, '%H:%M')

