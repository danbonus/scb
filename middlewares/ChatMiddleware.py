from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin

from vkbottle import MiddlewareResponse
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


class ChatMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin, scb):
        if message.peer_id != message.from_id:
            return MiddlewareResponse(False)