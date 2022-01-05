import random
from string import ascii_lowercase, digits


from repositories.repository import Repository
from repositories.time import TimeRepository


class WritersRepository(Repository):
    async def __init__(self, time: TimeRepository):
        super().__init__("writers")
        self.time = time

        #if user:
        #   self.request_id = (await self.get_last_request(uid=user.uid)).request_id

    async def get_current_writer(self):
        record = self._db.find_one({"timestamp": self.time.get_today()})
        if not record:

    async def choose_writer(self):
        model = {
            "timestamp": self.time.get_timestamp(),
            "writer": ...,
            "lessons_total": ...,
            "lessons_filled": ...,
            "filled_data": {}
        }
