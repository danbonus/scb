from logger import logger
import re
from utils.api import Api
import asyncio
from repositories.repository import Repository
from transliterate import translit
from models.bell import Bell


class GradesRepository(Repository):
    async def __init__(self, label=None, subjects=None):
        super().__init__("grades")
        self.label = label

        if label:
            self.record = await self._get_record()
            self.label = label
            self.id = self.record["id"]
            self.homework_db = self.record["homework_db"]
            self.album_id = self.record["album_id"]
            self.bells = {bell_num: Bell(data) for bell_num, data in self.record["bells"].items()}
            self.subjects = self.record["subjects"]
            self.schedule = self.record["schedule"]

    async def create(self, label, album_id, bells, subjects, schedule):
        pattern = re.compile('[\W_]+')
        scrapped_label = pattern.sub('', label).lower()
        scrapped_label = translit(scrapped_label, "ru", reversed=True)

        if not album_id:
            album_id = await Api.create_album(label)

        model = {
            "label": label,
            "id": scrapped_label,
            "homework_db": f"homework_{scrapped_label}",
            "album_id": album_id,
            "bells": bells,
            "subjects": subjects,
            "schedule": schedule
        }

        self._db.insert_one(model)

    async def _get_record(self):
        return await self._db.find_one({"label": self.label})

    @staticmethod
    async def get(label):
        return await GradesRepository(label)

    async def update(self, **info):
        await self._db.update_one({"label": self.label}, {"$set": {info}})

    async def delete(self):
        await self._db.delete_one({"label": self.label})

    @property  # в виде перемнной будет рекурсия
    async def list(self):
        result = self._db.find({})
        grades = [await GradesRepository(i["label"]) async for i in result]
        return grades

    async def is_grade(self, grade):
        for i in await self.list:
            if i.label.lower() == grade.lower():
                return True
        return False

    @classmethod
    async def refresh_grades(cls):
        """Creates new albums in new group."""
        available_grades = await cls.get_grades()
        logger.info("Refreshing grades")

        for grade in available_grades:
            logger.debug("Refreshing grade %s" % grade.label)
            new_id = await Api.create_album(grade.label)
            await grade.update_grade("album_id", new_id)
            await asyncio.sleep(1)

    async def new_group(self):
        pass

    async def get_homework_collection(self):
        pass
