from logger import logger
from models.replace import Replace
from repositories.grades import GradesRepository
from repositories.repository import Repository
from repositories.subjects import SubjectsRepository
from repositories.time import TimeRepository


class ReplacesRepository(Repository):
    async def __init__(self, grades: GradesRepository, subjects: SubjectsRepository, time: TimeRepository):
        super().__init__("replaces")
        self.grade = grades.id
        self.time = time

    async def create(self, timestamp, lesson, subject, replace_type, text):
        if not isinstance(timestamp, float):
            timestamp = self.time.timestamp_from_date(timestamp)

        last_record = await self._db.find_one(sort=[('timestamp', -1)])
        if not last_record:
            last_record = {"replace_id": 0}

        replace_id = int(last_record["replace_id"]) + 1

        model = {
            "replace_id": replace_id,
            "grade": self.grade,
            "timestamp": timestamp,
            "lesson": lesson,
            "subject": subject,
            "type": replace_type,
            "text": text,
        }
        await self._db.insert_one(model)

    async def _get_record(self):
        self._db.find_one()

    async def get(self, timestamp, lesson, subject):
        record = await self._db.find_one(
            {
                "grade": self.grade, "timestamp": timestamp, "lesson": lesson, "subject": subject
            }
        )
        if record:
            return Replace(record)

    async def get_for_day(self, timestamp):
        records = self._db.find({"grade": self.grade, "timestamp": timestamp})
        replaces = [Replace(i) async for i in records]
        logger.debug(replaces)
        logger.debug(timestamp)
        logger.debug(self.grade)
        return {i.lesson: i for i in replaces}

    async def update(self, **info):
        ...

    async def delete(self, timestamp, lesson, subject):
        await self._db.delete_one({"timestamp": timestamp, "lesson": lesson, "subject": subject})

    @property
    async def list(self):
        return

    def dict(self):  # доступ по лейблу из колбасок
        subjects = {}
        for subject in self.list_:
            subjects[subject.label] = subject
        return subjects

    def __getitem__(self, key):
        return self.dict[key]
