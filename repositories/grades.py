import asyncio
import re
from transliterate import translit

from logger import logger
from models.bell import Bell
from models.group import Group
from repositories.repository import Repository
from utils.api import Api


class GradesRepository(Repository):
    async def __init__(self, identifier=None, subjects=None):
        super().__init__("grades")
        self.id = identifier

        if identifier:
            self.record = await self._get_record()
            self.label = self.record["label"]
            self.id = self.record["id"]
            self.homework_db = self.record["homework_db"]
            self.album_id = self.record["album_id"]
            self.bells = {bell_num: Bell(data) for bell_num, data in self.record["bells"].items()}
            self.subjects = self.record["subjects"]
            self.schedule = self.record["schedule"]
            self.lang_groups = [Group(i) for i in self.record["lang_groups"]]
            self.exam_groups = [Group(i) for i in self.record["exam_groups"]]

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
        return await self._db.find_one({"id": self.id})

    @staticmethod
    async def get(identifier):
        return await GradesRepository(identifier)

    async def update(self, **info):
        await self._db.update_one({"id": self.id}, {"$set": {info}})

    async def delete(self):
        await self._db.delete_one({"id": self.id})

    @property  # в виде перемнной будет рекурсия
    async def list(self):
        result = self._db.find({})
        grades = [await GradesRepository(i["id"]) async for i in result]
        return grades

    async def is_grade(self, grade):
        for i in await self.list:
            if i.label.lower() == grade.lower():
                return i

    async def is_group(self, groups, group):
        if not group.isdigit():
            return False
        for i in groups:
            if int(i.num) == int(group):
                return i

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
