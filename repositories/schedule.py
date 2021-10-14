from logger import logger
from utils.async_object import AsyncObject
import re
from vkbottle import CtxStorage
from utils.api import Api
import asyncio
from repositories.repository import Repository
from repositories.grades import GradesRepository


class ScheduleRepository(Repository):
    async def __init__(self, grades: GradesRepository):
        super().__init__("schedule")
        self.grades = grades
        self.bells_time = {
            0: ["8:05", "8:50"],
            1: ["9:00", "9:45"],
            2: ["10:05", "10:50"],
            3: ["11:10", "11:55"],
            4: ["12:10", "12:55"],
            5: ["13:10", "13:55"],
            6: ["14:10", "14:55"],
            7: ["15:05", "15:50"]
        }
        self.yesterday = ...
        self.current_day = ...
        self.tomorrow_day = ...

    async def create(self, **info ):
        model = {
            "monday": ...,
            "tuesday": ...,
            "wednesday": ...,
            "thursday": ...,
            "friday": ...,
            "saturday": ...,
            "sunday": ...
        }
        await self.grades.update(schedule=model)

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
