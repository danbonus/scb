from logger import logger
from utils.async_object import AsyncObject
import re
from vkbottle import CtxStorage
from utils.api import Api
import asyncio


class GradesRepository(AsyncObject):
    async def __init__(self, label=None):
        storage = CtxStorage()
        self.db = storage.get("db").grades
        if label:
            self.record = await self.db.find_one({"label": label})
            self.label = label
            self.id = self.record["id"]
            self.homework_db = self.record["homework_db"]
            self.album_id = self.record["album_id"]
        
    @classmethod
    async def is_grade(cls, grade):
        for i in await cls.get_grades():
            if i.label.lower() == grade.lower():
                return True
        return False
    
    @classmethod
    async def get_grades(cls):
        result = (await cls()).db.find({})
        grades = [await cls(i["label"]) async for i in result]
        return grades
    
    @classmethod
    async def make_grade(cls, label, album_id=None):
        pattern = re.compile('[\W_]+')
        scrapped_label = pattern.sub('', label).lower()

        if not album_id:
            album_id = await Api.create_album(label)
            
        model = {
            "label": label,
            "id": scrapped_label,
            "homework_db": f"homework_{scrapped_label}",
            "album_id": album_id
        }

        cls().db.insert_one(model)

    async def delete_grade(self):
        await self.db.delete_one({"label": self.label})

    async def update_grade(self, keyword, value):
        await self.db.update_one({"label": self.label}, {"$set": {keyword: value}})

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

