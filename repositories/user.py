from logger import logger
from models.user import user
from repositories.repository import Repository
from repositories.requests import RequestsRepository


class UserRepository(Repository):
    async def __init__(self, uid: int, case="nom", on_event=False):
        #logger.spam("User Repository init")
        super().__init__("users")
        self.uid = uid
        self.new = False
        self.record = await self._get_record()

        self.grade = self.record["grade"]
        self.lang_group = self.record["lang_group"]
        self.exam_group = self.record["exam_group"]
        self.registered = self.grade

        self.lang = self.record["lang"]

        self.is_broadcast_subscriber = self.record["broadcast_user"]
        self.broadcast_time = self.record["broadcast_time"]

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

    async def register(self, grade, lang_group, exam_group):
        await self.update(grade=grade, lang_group=lang_group, exam_group=exam_group, registered=True)

    async def set_broadcast(self, broadcast_user, broadcast_time):
        await self.update(broadcast_user=broadcast_user, broadcast_time=broadcast_time)
