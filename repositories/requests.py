from repositories.repository import Repository
from logger import logger
from string import ascii_lowercase, digits
import random


class RequestsRepository(Repository):
    async def __init__(self, request_id=None):
        super().__init__("requests")
        self.request_id = request_id
        self.record = await self._get_record()

        if not self.record:
            self.record = {
                "request_id": 0,
                "uid": 0,
                "message": 0,
                "timestamp": 0
            }

        self.uid = self.record["uid"]
        self.request_id = self.record["request_id"]
        self.message = self.record["message"]
        # self.handler = self.record["handler"]
        self.timestamp = self.record["timestamp"]

    async def create(self, message):
        alphabet = ascii_lowercase + digits
        request_id = ''.join(random.choices(alphabet, k=8))

        await self._db.insert_one(
            {
                "request_id": request_id,
                "uid": message.from_id,
                "message": message.text,
                "timestamp": message.date
            }
        )

    async def _get_record(self):
        #print(self.request_id)
        return await self._db.find_one({"request_id": self.request_id})

    @staticmethod
    async def get(request_id):
        return await RequestsRepository(request_id)

    async def update(self, **info):
        self._db.update_one({"request_id": self.request_id}, {"$set": info})

    async def delete(self):
        pass

    @classmethod
    async def get_last_request(cls, **info):
        last_request = await (await cls())._db.find_one(info, sort=[("timestamp", -1)])
        if not last_request:
            last_request = {
                "request_id": 0
            }
        #logger.debug(last_request)
        return await RequestsRepository(last_request["request_id"])
