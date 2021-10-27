from utils.async_object import AsyncObject
from motor.core import Collection


class Repository(AsyncObject):
    db = None

    def __init__(self, collection):
        #storage = CtxStorage()
        #self._db = storage.get("db")[db]
        self._db: Collection = self.db[collection]

    async def create(self, *args, **kwargs):
        ...

    async def _get_record(self):
        ...

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
