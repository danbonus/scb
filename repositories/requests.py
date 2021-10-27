from repositories.repository import Repository
from logger import logger
from string import ascii_lowercase, digits
import random


class RequestsRepository(Repository):
    async def __init__(self, request_id=None, user=None):
        super().__init__("requests")
        self.request_id = request_id

        #if user:
        #   self.request_id = (await self.get_last_request(uid=user.uid)).request_id

        self.record = await self._get_record()

        if not self.record:
            self.record = {
                "request_id": 0,
                "uid": 0,
                "message": 0,
                "timestamp": 0,
                "handler": "Not handled yet",
                "return_command": False,
                "event": {},
                "state": None
            }

        self.uid = self.record["uid"]
        self.request_id = self.record["request_id"]
        self.message = self.record["message"]
        self.timestamp = self.record["timestamp"]
        self.handler = self.record["handler"]
        self.return_command = self.record["return_command"]
        self.event = self.record["event"]

    @classmethod
    async def create(cls, message, event):
        alphabet = ascii_lowercase + digits
        request_id = ''.join(random.choices(alphabet, k=8))

        await (await cls())._db.insert_one(
            {
                "request_id": request_id,
                "uid": message.from_id,
                "message": message.text,
                "timestamp": message.date,
                "handler": "not handled yet",
                "return_command": False,
                "event": event,
                "state": message.state_peer.state if message.state_peer else message.state_peer
            }
        )
        return request_id

    async def _get_record(self):
        #print(self.request_id)
        return await self._db.find_one({"request_id": self.request_id})

    @staticmethod
    async def get(request_id):
        return await RequestsRepository(request_id)

    async def update(self, **info):
        #request_id = (await self.get_last_request(uid=self.uid)).request_id
        self._db.update_one({"request_id": self.request_id}, {"$set": info})

    async def delete(self):
        pass

    @classmethod
    async def get_last_request(cls, **info):
        last_record = await (await cls())._db.find_one(info, sort=[("timestamp", -1)])
        if not last_record:
            last_record = {
                "request_id": 0
            }
        #logger.debug(last_request)
        logger.info(last_record["request_id"])
        last_request: RequestsRepository = await RequestsRepository(request_id=last_record["request_id"])
        return last_request

    async def get_penultimate_request(self):
        last_record = await self._db.find({"uid": self.uid}, sort=[("timestamp", -1)]).to_list(2)
        last_record = last_record[1]
        # logger.debug(last_request)
        last_request: RequestsRepository = await RequestsRepository(last_record["request_id"])
        return last_request

    async def get_request_by_index(self, record_num):
        records = await self._db.find(
            {"uid": self.uid, "return_command": False}, sort=[("timestamp", -1)]
        ).to_list(15)
        last_record = records[record_num]
        # logger.debug(last_request)
        last_request: RequestsRepository = await RequestsRepository(last_record["request_id"])
        return last_request

    async def get_last_requests_by_count(self, num_skip, num):
        records = await self._db.find({"uid": self.uid, "return_command": False}, sort=[("timestamp", -1)]).skip(num_skip).to_list(num)
        #logger.error("Getting Records: %s" % records)
        # logger.debug(last_request)
        #requests: List[RequestsRepository] = [await RequestsRepository(record["request_id"]) for record in records]
        return records

    async def get_stateless_requests_by_count(self, num_skip, num):
        records = await self._db.find({"uid": self.uid, "return_command": False, "state": None}, sort=[("timestamp", -1)]).skip(num_skip).to_list(num)
        # logger.debug(last_request)
        #requests: List[RequestsRepository] = [await RequestsRepository(record["request_id"]) for record in records]
        return records
