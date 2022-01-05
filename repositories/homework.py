from datetime import timedelta
from typing import List, Tuple

from logger import logger
from models.expanded_homework_record import ExpandedHomeworkRecord
from models.homework_record import HomeworkRecord
from models.lesson import Lesson
from models.schedule_element import ScheduleElement
from repositories.replaces import ReplacesRepository
from repositories.repository import Repository
from repositories.schedule import ScheduleRepository
from repositories.time import TimeRepository
from repositories.user import UserRepository
from utils.api import Api


class HomeworkRepository(Repository):
    async def __init__(self, schedule: ScheduleRepository, time: TimeRepository, api: Api, user: UserRepository, replaces: ReplacesRepository, homework_db=None):
        super().__init__(homework_db)
        self.schedule = schedule
        self.time = time
        self.api = api
        self.user = user
        self.replaces = replaces
        self.record = await self._get_record()
        self.model = {
            "homework_id": "-",
            "subject": None,
            "homework": "ещё неизвестно.",
            'attachments': [],
            "gdz": None,
            "timestamp": None,
            "sender": None
        }

    async def create(self, subjects, homework, attachments, to, sender):
        models = []
        if not isinstance(subjects, list):
            subjects = [subjects]

        for subject in subjects:
            if isinstance(to, str):
                to = self.time.timestamp_from_date(to)
            else:
                logger.critical("No TO")
                to = self.next_lesson(subject)

            logger.debug("To: %s" % to)

            last_record = await self._db.find_one(sort=[('homework_id', -1)])
            if not last_record:
                last_record = {"homework_id": 0}

            hw_id = int(last_record["homework_id"]) + 1

            last_day, next_day = self.time.get_days_of_school()

            model = {
                "homework_id": hw_id,
                "subject": subject,
                "homework": homework,
                'attachments': attachments,
                "gdz": [],
                "timestamp": self.previous_lesson(subject, last_day),
                "real_timestamp": self.time.get_timestamp(),
                "to": to,
                "sender": sender
            }

            await self._db.insert_one(model)
            models.append(model)

        return models

    async def _get_record(self):
        self._db.find_one()

    @staticmethod
    async def get(name):
        ...

    async def update(self, **info):
        ...

    async def delete(self, homework_id):
        print(homework_id)
        record = await self._db.find_one({"homework_id": homework_id})
        print(record)
        message = "ok\n"
        if not record:
            return ("⚠️ | Не удалось произвести удаление записи!\n"
                    "Причина: не найдена исходная запись.")

        if record['attachments']:
            for photo_id in record['attachments']:
                try:
                    await self.api.user_api.photos.delete(photo_id=photo_id)
                    message += f"✔ | Фотография была успешно удалена из альбома {self.user.grade}!"
                except Exception as exc:
                    message += f"⚠ | Не удалось произвести удаление фотографии из альбома {self.user.grade}: %s" % exc

        await self._db.delete_one({"homework_id": homework_id})
        return message


    async def get_last_homework(self, subject):
        found_subject = await self._db.find_one({"subject": subject}, sort=[('timestamp', -1)])
        if found_subject:
            return HomeworkRecord(found_subject)

    def previous_lesson(self, subject, date):
        #this_day, tomorrow_day = self.time.get_days_of_school()
        print('current date: %s' % date)
        this_day_weekday = date.weekday()
        print('current weekday: %s' % this_day_weekday)
        on_week = []
        for day, schedule in self.schedule.schedule.items():
            for lesson in schedule:
                if lesson.subject.label == subject:
                    on_week.append(int(day))
        print("on_week: %s" % on_week)
        if on_week[0] > this_day_weekday:
            print('last week')
            delta = this_day_weekday - on_week[-1]
            print(delta)
            print(abs(delta))
            date = date + timedelta(days=abs(delta))
            date = date - timedelta(days=7)
        else:
            print("current week")
            for i in on_week[::-1]:
                if i <= this_day_weekday:
                    print(f"текущий день недели {this_day_weekday} больше чем {i}")
                    delta = this_day_weekday - i
                    print(delta)
                    date = date - timedelta(delta)
                    print("date: %s" % date)
                    break
        return int(date.timestamp())

    def next_lesson(self, subject):
        this_day, tomorrow_day = self.time.get_days_of_school()
        this_day_weekday = this_day.weekday()
        print("This day: %s" % this_day_weekday)
        logger.debug(subject)
        subject_on_week = []
        for day, schedule in self.schedule.schedule.items():
            for lesson in schedule:
                if lesson.subject.label == subject:
                    subject_on_week.append(day)
        print("Кол-во уроков: %s" % len(subject_on_week))
        print("Предметы по дням недели: %s" % ', '.join(subject_on_week))
        last_lesson_on_week = int(subject_on_week[-1])
        print("ПОследний урок на неделе: %s" % last_lesson_on_week)

        if this_day_weekday >= last_lesson_on_week:
            print("Урок будет на след. неделе")
            # date = pendulum.instance(this_day).next(int(subject_on_week[0]))
            print((int(subject_on_week[0]) - this_day_weekday) % 7)
            date = this_day + timedelta(days=(int(subject_on_week[0]) - this_day_weekday) % 7)

        else:
            next_ = None
            for i in subject_on_week:
                if int(i) > this_day_weekday:
                    next_ = int(i)
                    break
            print("Следующий урок: %s" % next_)
            print("Урок будет на этой неделе")
            date = this_day + timedelta(days=next_ - this_day_weekday)
        return int(date.timestamp())

    @property
    async def list(self):
        return

    async def nameitlater(self, date=None) -> Tuple[List[Lesson], List[Lesson]]:
        return await self.for_today(date), await self.for_tomorrow(date)

    async def for_today(self, date=None):
        this_day, tomorrow_day, start_ts, end_ts = await self.get_time(date)
        replaces = await self.replaces.get_for_day(this_day.timestamp())
        today_schedule = self.schedule.schedule[str(this_day.weekday())]

        for_today = [i async for i in self.get_homework(
            today_schedule, replaces, date=this_day
        )]

        return for_today

    async def for_tomorrow(self, date=None):
        this_day, tomorrow_day, start_ts, end_ts = await self.get_time(date)

        replaces = await self.replaces.get_for_day(tomorrow_day.timestamp())
        tomorrow_schedule = self.schedule.schedule[str(tomorrow_day.weekday())]

        for_tomorrow = [i async for i in self.get_homework(tomorrow_schedule, replaces, to=tomorrow_day.timestamp())]

        return for_tomorrow

    async def get_time(self, date=None):
        logger.debug("Getting time: %s" % date)
        this_day, tomorrow_day = self.time.get_days_of_school(date)
        logger.debug("Tomorrow day: %s" % tomorrow_day)
        start_ts, end_ts = self.time.get_day_time_borders(this_day)
        return this_day, tomorrow_day, start_ts, end_ts

    async def get_homework(self, schedule: List[ScheduleElement], replaces, **kwargs):
        logger.debug("Your replaces: %s" % replaces)
        logger.debug("Your schedule: %s" % [i.subject for i in schedule])
        logger.debug("Timestamp: %s" % kwargs)
        for schedule_element in schedule:
            if schedule_element.bell in replaces:
                logger.debug(schedule_element.subject)
                if schedule_element.subject.label == replaces[schedule_element.bell].subject:
                    schedule_element.replace = replaces[schedule_element.bell]
            logger.debug(schedule_element.subject)
            subject = schedule_element.subject.label
            if 'to' in kwargs:
                print(kwargs)
                found_subject = await self.get_record(subject, **kwargs)
            else:
                found_subject = await self.get_record(subject, **{"timestamp": self.previous_lesson(subject, date=kwargs['date'])})
            print(found_subject)
            if found_subject:
                homework_record = HomeworkRecord(found_subject)

            else:
                model = self.model
                model["subject"] = subject
                homework_record = HomeworkRecord(model)

            yield Lesson(homework_record, schedule_element)

    async def get_record(self, subject, **kwargs):
        found_subject = await self._db.find_one({"subject": subject, **kwargs}, sort=[("homework_id", -1)])
        return found_subject

    async def get_by_id(self, homework_id):
        found_subject = await self._db.find_one({"homework_id": homework_id}, sort=[("homework_id", -1)])
        return HomeworkRecord(found_subject)

    async def get_records(self, subjects_rep, offset):
        plain_records = self._db.find(sort=[("homework_id", -1)]).skip(offset).limit(8)
        count = await self._db.count_documents(filter={"homework_id": {"$exists": True}})
        print(count)
        print(offset)
        records = [ExpandedHomeworkRecord(i, subjects_rep[i['subject']]) async for i in plain_records]
        print(records)
        return count, records

    async def get_filled(self, date=None):
        for i in await self.for_today(date):
            #logger.warning(i.subject.label)
            if str(i.homework.homework_id).isdigit():
                #logger.debug("Passed")
                yield i.subject
        for i in await self.for_tomorrow(date):
            if str(i.homework.homework_id).isdigit():
                #logger.debug("Passed")
                yield i.subject

    async def get_last_homework_requests(self, requests):
        this_day, tomorrow_day = self.time.get_days_of_school()
        homework_requests = []
        if self.time.get_today().weekday() in [0, 6]:
            for i in requests:
                request_date = self.time.get_date_from_timestamp(i.timestamp)
                if request_date.weekday() == 5:
                    if request_date.hour > 8:
                        homework_requests.append(i)
                elif request_date.weekday() == 6:
                    if self.time.get_today().weekday() == 6:
                        homework_requests.append(i)
                    if self.time.get_today().weekday() == 0 and self.time.get_today().hour < 8:
                        homework_requests.append(i)
                elif request_date.weekday() == 0:
                    if request_date.hour < 8 and self.time.get_today().hour < 8:
                        homework_requests.append(i)
                    elif request_date.hour >= 8 and self.time.get_today().hour >= 8:
                        homework_requests.append(i)

            '''list(
                filter(
                    lambda i: self.time.get_start_timestamp(i.timestamp) == self.time.get_start_timestamp(
                        self.time.get_today().timestamp()
                    ), requests
                )
            )'''
        else:
            homework_requests = list(
                filter(
                    lambda i: self.time.get_start_timestamp(i.timestamp) == int(this_day.timestamp()), requests
                )
            )

        return homework_requests
