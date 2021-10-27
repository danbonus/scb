from repositories.repository import Repository
from repositories.schedule import ScheduleRepository
from utils.my_time import MyTime
from models.lesson import Lesson
from models.homework_record import HomeworkRecord
import time
from logger import logger


class HomeworkRepository(Repository):
    async def __init__(self, schedule: ScheduleRepository, time: MyTime, homework_db=None):
        super().__init__(homework_db)
        self.schedule = schedule
        self.time = time
        self.record = await self._get_record()
        self.model = {
            "homework_id": None,
            "subject": None,
            "homework": "",
            'attachments': None,
            "gdz": None,
            "timestamp": None,
            "sender": None,
        }

    async def create(self, **info):
        model = {
            "homework_id": 0,
            "subject": info["subject"],
            "homework": info["homework"],
            'attachments': info["attachments"],
            "gdz": [],
            "timestamp": int(time.time()),
            "sender": info["sender"],
        }

        await self._db.insert_one(model)

    async def _get_record(self):
        self._db.find_one()

    @staticmethod
    async def get(name):
        ...

    async def update(self, **info):
        ...

    async def delete(self):
        ...

    @property
    async def list(self):
        return

    @property
    async def for_today(self):
        this_day, tomorrow_day = self.time.check_for_weekday()
        return self.get_records(this_day, self.schedule.today)

    @property
    async def for_tomorrow(self):
        this_day, tomorrow_day = self.time.check_for_weekday()
        return self.get_records(tomorrow_day, self.schedule.tomorrow)


    async def get_records(self, day, schedule):
        start_ts, end_ts = self.time.start_end(day)

        for schedule_element in schedule:
            logger.debug(schedule_element)
            subject = schedule_element.subject.label
            found_subject = await self._db.find_one({"subject": subject, "timestamp": {"$gt": start_ts, "$lt": end_ts}})
            print(found_subject)
            if found_subject:
                homework_record = HomeworkRecord(found_subject)

            else:
                model = self.model
                model["homework"] = "ещё неизвестно."
                model["subject"] = subject
                homework_record = HomeworkRecord(model)

            yield Lesson(homework_record, schedule_element)