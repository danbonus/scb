from motor.core import Collection

from utils.async_object import AsyncObject


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

    async def get(name, *args, **kwargs):
        ...

    async def update(self, **info):
        ...

    async def delete(self, *args, **kwargs):
        ...

    @property
    async def list(self):
        return
