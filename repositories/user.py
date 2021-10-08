from vkbottle import CtxStorage
from models.user import user
from logger import logger
from utils.async_object import AsyncObject


class UserRepository(AsyncObject):
    async def __init__(self, uid: int, case="nom"):
        storage = CtxStorage()
        self.db = storage.get("db")
        self.uid = uid
        self.record = await self.get_record()
        self.newbie = False

        if "first_entry" in self.record:
            self.newbie = True

        self.registered = self.record["registered"]
        self.grade = self.record["grade"]
        self.lang = self.record["lang"]
        self.is_writer = self.record["is_writer"]
        self.is_admin = self.record["is_admin"]
        self.first_name = self.record["name_cases"][case]["first_name"]
        self.last_name = self.record["name_cases"][case]["last_name"]
        self.full_name = self.record["name_cases"][case]["full_name"]
        self.blocked = self.record["blocked"]

    async def create_new(self):
        logger.debug("New user! Creating a record.")
        user_model = await user(uid=self.uid)
        print(user_model)
        await self.db.users.insert_one(user_model)
        return await self.get_record()

    async def get_record(self):
        result = await self.db.users.find_one({"uid": self.uid})

        if not result:
            result = await self.create_new()

        return result

    async def update_user(self, info: dict):
        await self.db.users.update_one({"uid": self.uid}, info)

    async def register(self, grade):
        self.grade = grade
        await self.db.users.update_one({"uid": self.uid}, {"grade": grade, "registered": True})

    async def not_newbie_anymore(self):
        await self.db.users.update_one({"uid": self.uid}, {"$unset": {"first_entry": True}})
