import random
from string import ascii_lowercase, digits
from typing import List, Union

from datetime import datetime, time

from repositories.repository import Repository


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
    async def create(cls, from_id, text, date, state_peer, event):
        alphabet = ascii_lowercase + digits
        request_id = ''.join(random.choices(alphabet, k=8))

        await (await cls())._db.insert_one(
            {
                "request_id": request_id,
                "uid": from_id,
                "message": text,
                "timestamp": date,
                "handler": "not handled yet",
                "return_command": False,
                "event": event,
                "state": state_peer.state if state_peer else 0
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
        #logger.info(last_record["request_id"])
        last_request: RequestsRepository = await RequestsRepository(request_id=last_record["request_id"])
        return last_request

    async def get_last_handler_by_label(self, uid, handlers) -> Union[List["RequestsRepository"], List]:
        end = datetime.today().timestamp()  #
        start = end - 86400
        requests = []
        for i in handlers:
            last_handler = await self._db.find_one({"uid": uid, "handler": i, "timestamp": {"$gt": start, "$lt": end}}, sort=[("timestamp", -1)])
            if last_handler:
                requests.append(last_handler)
                break

        #if requests:
        #    return [await RequestsRepository(request_id=i["request_id"]) for i in requests]
        return [await RequestsRepository(request_id=i["request_id"]) for i in requests]
