from vkbottle import MiddlewareResponse
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware
from logger import logger
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin


class UserBlockedMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin, scb):
        if scb.user.is_blocked:
            logger.info("User is blocked! Passing.")
            return MiddlewareResponse(False)
