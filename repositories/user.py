from models.user import user
from logger import logger
from repositories.requests import RequestsRepository
from repositories.repository import Repository


class UserRepository(Repository):
    async def __init__(self, uid: int, case="nom", on_event=False):
        #logger.spam("User Repository init")
        super().__init__("users")
        self.uid = uid
        self.new = False
        self.record = await self._get_record()

        self.grade = self.record["grade"]
        self.lang_group = self.record["lang_group"]
        self.ege_group = self.record["ege_group"]
        self.registered = self.grade

        self.lang = self.record["lang"]

        self.broadcast_info = self.record["broadcast_info"]
        self.is_broadcast_subscriber = self.record["broadcast_user"]
        self.broadcast_type = self.broadcast_info["type"]
        self.broadcast_time = self.broadcast_info["time"]

        self.roles = self.record["roles"]
        self.is_writer = self.roles["writer"]
        self.is_admin = self.roles["admin"]
        self.is_blocked = self.roles["blocked"]

        self.first_name = self.record["name_cases"][case]["first_name"]
        self.last_name = self.record["name_cases"][case]["last_name"]
        self.full_name = self.record["name_cases"][case]["full_name"]

        self.last_request = await RequestsRepository.get_last_request(uid=self.uid)

    async def create(self):
        record = await user(uid=self.uid)

        await self._db.insert_one(record)
        return record

    async def _get_record(self):
        record = await self._db.find_one({"uid": self.uid})

        if not record:
            print(self.uid)
            logger.debug("New user! Creating a record.")
            self.new = True
            record = await self.create()

        return record

    @staticmethod
    async def get(uid, case=None) -> "UserRepository":
        return await UserRepository(uid, case)

    async def update(self, **info):
        await self._db.update_one({"uid": self.uid}, {"$set": info})

    async def delete(self):
        await self._db.delete_one({"uid": self.uid})

    async def register(self, grade):
        await self.update(grade=grade, registered=True)

    async def set_broadcast(self, **broadcast_info):
        await self.update(broadcast_user=True, broadcast_info=broadcast_info)
