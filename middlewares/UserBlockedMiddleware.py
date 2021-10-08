from vkbottle import BaseMiddleware, MiddlewareResponse
from logger import logger
from repositories.user import UserRepository
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin


class UserBlockedMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin):
        user = await UserRepository(message.from_id)
        logger.info("Got a message from %s: %s" % (user.full_name, message.text))

        if user.blocked:
            logger.info("User is blocked! Passing.")
            return MiddlewareResponse(False)
