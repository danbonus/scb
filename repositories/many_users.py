from .user import UserRepository
from logger import logger
from vkbottle_overrides.tools import CtxStorage


class ManyUsersRepository:
    """Interface to work with user collections. Not inheriting the main Repository class"""
    @classmethod
    async def get_admins(cls):
        return await cls.get_many("is_admin", True)

    @classmethod
    async def get_owners(cls):
        return await cls.get_many("is_owner", True)

    @classmethod
    async def get_writers(cls):
        return await cls.get_many("is_writer", True)

    @classmethod
    async def get_many(cls, keyword, value):
        db = CtxStorage().get("db")
        users = []
        result = db.users.find({keyword: value})

        async for i in result:
            current_user = await UserRepository(i["uid"])
            users.append(current_user)

        logger.debug("Getting users by %s keyword: found %s" % (keyword, len(users)))

        return users
