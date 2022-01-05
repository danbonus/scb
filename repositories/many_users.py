from typing import List

from logger import logger
from vkbottle_overrides.tools import CtxStorage
from .user import UserRepository


class ManyUsersRepository:
    """Interface to work with user collections. Not inheriting the main Repository class"""
    @classmethod
    async def get_admins(cls):
        return await cls.get_many(
            "roles",
            {
                "writer": False,
                "admin": True,
                "blocked": False
            }
                                  )

    @classmethod
    async def get_owners(cls):
        return await cls.get_many(
            "roles",
            {
                "writer": True,
                "admin": True,
                "blocked": False
            }
        )

    @classmethod
    async def get_writers(cls):
        return await cls.get_many(
            "roles",
            {
                "writer": True,
                "admin": False,
                "blocked": False
            }
                                  )

    @classmethod
    async def get_broadcast_subscribers(cls):
        return await cls.get_many("broadcast_user", True)

    @classmethod
    async def get_many(cls, keyword, value) -> List[UserRepository]:
        db = CtxStorage().get("db")
        users = []

        result = db.users.find({keyword: value})

        async for i in result:
            current_user = await UserRepository(i["uid"])
            users.append(current_user)

        logger.debug("Getting users by %s keyword and %s value: found %s" % (keyword, value, len(users)))

        users.sort(key=lambda user: user.last_name)

        return users
