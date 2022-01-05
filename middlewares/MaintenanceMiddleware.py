from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin

from vkbottle import MiddlewareResponse
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


class MaintenanceMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin, scb):
        maintenance = False
        if maintenance and message.peer_id != 0:
            await message.answer("Техработы. Повторите попытку позже. Беу.")
            return MiddlewareResponse(False)
