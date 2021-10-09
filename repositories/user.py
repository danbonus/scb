from vkbottle import CtxStorage
from models.user import user
from logger import logger
from utils.async_object import AsyncObject


class UserRepository(AsyncObject):
    async def __init__(self, uid: int, case="nom"):
        logger.spam("User Repository init")
        storage = CtxStorage()
        self.db = storage.get("db")
        self.uid = uid
        self.new = False
        self.record = await self.get_record()

        self.grade = self.record["grade"]
        self.registered = self.grade

        self.lang = self.record["lang"]

        self.broadcast_info = self.record["broadcast_info"]
        self.is_broadcast_subscriber = self.broadcast_info["subscriber"]
        self.broadcast_type = self.broadcast_info["type"]
        self.broadcast_time = self.broadcast_info["time"]

        self.roles = self.record["roles"]
        self.is_writer = self.roles["writer"]
        self.is_admin = self.roles["admin"]
        self.is_blocked = self.roles["blocked"]

        self.first_name = self.record["name_cases"][case]["first_name"]
        self.last_name = self.record["name_cases"][case]["last_name"]
        self.full_name = self.record["name_cases"][case]["full_name"]


    async def get_record(self):
        record = await self.db.users.find_one({"uid": self.uid})

        if not record:
            logger.debug("New user! Creating a record.")
            self.new = True
            record = await user(uid=self.uid)

            await self.db.users.insert_one(record)

        return record

    async def update_user(self, **info):
        await self.db.users.update_one({"uid": self.uid}, {"$set": info})

    async def register(self, grade):
        await self.update_user(grade=grade, registered=True)

    async def set_broadcast(self, **broadcast_info):
        await self.update_user(broadcast_info=broadcast_info)
