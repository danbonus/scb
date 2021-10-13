from logger import logger
from utils.async_object import AsyncObject
import re
from vkbottle import CtxStorage
from utils.api import Api
import asyncio
from repositories.repository import Repository


class ScheduleRepository(Repository):
    async def __init__(self, grade=None):
        super().__init__("schedule")
        self.grade = grade

    async def create(self, *args, **kwargs):
        self._db.insert_one()

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
