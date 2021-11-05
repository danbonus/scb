from repositories.repository import Repository
from repositories.schedule import ScheduleRepository
from models.lesson import Lesson
from models.homework_record import HomeworkRecord
from logger import logger
import datetime
from datetime import timedelta
from repositories.time import TimeRepository
from repositories.user import UserRepository
from utils.api import Api
from typing import List, Tuple


class HomeworkRepository(Repository):
    async def __init__(self, schedule: ScheduleRepository, time: TimeRepository, api: Api, user: UserRepository, homework_db=None):
        super().__init__(homework_db)
        self.schedule = schedule
        self.time = time
        self.api = api
        self.user = user
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
            if not to:
                logger.critical("No TO")
                to = self.next_lesson(subject)

            logger.debug("To: %s" % to)

            last_record = await self._db.find_one(sort=[('timestamp', -1)])
            if not last_record:
                last_record = {"homework_id": 0}

            hw_id = int(last_record["homework_id"]) + 1

            model = {
                "homework_id": hw_id,
                "subject": subject,
                "homework": homework,
                'attachments': attachments,
                "gdz": [],
                "timestamp": self.time.get_timestamp(),
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
        record = await self._db.homework.find_one({"homework_id": homework_id})
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

        await self._db.homework.delete_one({"homework_id": homework_id})


    async def get_last_homework(self, subject):
        found_subject = await self._db.find_one({"subject": subject}, sort=[('timestamp', -1)])
        if found_subject:
            return HomeworkRecord(found_subject)

    def next_lesson(self, subject):
        this_day, tomorrow_day = self.time.get_days_of_school()
        this_day_weekday = this_day.weekday()
        print("This day: %s" % this_day_weekday)

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
        return date.strftime("%d.%m.%y")

    @property
    async def list(self):
        return

    async def nameitlater(self, date=None) -> Tuple[List[Lesson], List[Lesson]]:
        return await self.for_today(date), await self.for_tomorrow(date)

    async def for_today(self, date=None):
        this_day, tomorrow_day, start_ts, end_ts = await self.get_time(date)
        today_schedule = self.schedule.schedule[str(this_day.weekday())]
        for_today = [i async for i in self.get_homework(
            today_schedule, timestamp={"$gt": start_ts, "$lt": end_ts}
        )]
        return for_today

    async def for_tomorrow(self, date=None):
        this_day, tomorrow_day, start_ts, end_ts = await self.get_time(date)

        tomorrow_schedule = self.schedule.schedule[str(tomorrow_day.weekday())]
        for_tomorrow = [i async for i in self.get_homework(tomorrow_schedule, to=tomorrow_day.strftime("%d.%m.%y"))]
        return for_tomorrow

    async def get_time(self, date):
        this_day, tomorrow_day = self.time.get_days_of_school(date)
        #if date:
        #    this_day = datetime.datetime.strptime(date, "%d.%m.%Y")
        #    tomorrow_day = this_day + datetime.timedelta(days=1)
        #    print(tomorrow_day)

        start_ts, end_ts = self.time.get_day_time_borders(this_day)
        return this_day, tomorrow_day, start_ts, end_ts

    async def get_homework(self, schedule, **kwargs):
        for schedule_element in schedule:
            #logger.debug(schedule_element)
            subject = schedule_element.subject.label
            found_subject = await self.get_record(subject, **kwargs)
            #print(found_subject)
            if found_subject:
                homework_record = HomeworkRecord(found_subject)

            else:
                model = self.model
                model["subject"] = subject
                homework_record = HomeworkRecord(model)

            yield Lesson(homework_record, schedule_element)

    async def get_record(self, subject, **kwargs):
        found_subject = await self._db.find_one({"subject": subject, **kwargs}, sort=[("timestamp", -1)])
        return found_subject

    async def get_filled_for_today(self, date=None):
        for i in await self.for_today(date):
            #logger.warning(i.subject.label)
            if str(i.homework.homework_id).isdigit():
                #logger.debug("Passed")
                yield i.subject
