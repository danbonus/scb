from datetime import datetime, time, timedelta


class MyTime:
    def __init__(self):
        self.night = "night"
        self.morning = "morning"
        self.afternoon = "afternoon"
        self.evening = "evening"

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
        this_day = datetime.date(datetime.today())
        tomorrow_day = datetime.date(datetime.today() + timedelta(days=1))

        if weekday == 0:  # Понедельник
            this_day = datetime.date(datetime.today() - timedelta(days=2))
        elif weekday == 5:  # Суббота
            tomorrow_day = datetime.date(datetime.today() + timedelta(days=2))
        elif weekday == 6:
            this_day = datetime.date(datetime.today() - timedelta(days=1))
            return this_day, tomorrow_day

        if hour < 8:
            this_day = datetime.date(datetime.today() - timedelta(days=1))
            tomorrow_day = datetime.date(datetime.today())

        return this_day, tomorrow_day

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
        midnight = datetime.combine(datetime.today(), time.min)
        start = int(midnight.timestamp())
        end = start + 83699
        if start < timestamp < end:
            return True

    def start_end(self, date=None):
        midnight = datetime.combine(datetime.today() if not date else date, time.min)
        start = int(midnight.timestamp())
        end = start + 111600
        return start, end

    @property
    def now(self):
        return datetime.now()

    def hm_format(self, message):
        datetime.strptime(message, '%H:%M')

my_time = MyTime()
