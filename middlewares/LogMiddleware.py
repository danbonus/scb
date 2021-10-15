from vkbottle import ABCView
from logger import logger
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from vkbottle.bot import Message
from typing import List, Any
from utils.args_object import SCB

from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


class LogMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin, scb: SCB):
        print()
        logger.info("Got a message from %s: %s" % (scb.user.full_name, message.text))
        await scb.requests.create(message)

    async def post(
            self,
            message: Message,
            view: "ABCView",
            handle_responses: List[Any],
            handlers: List["FromFuncHandler"],
    ):
        if not handlers:
            return

        logger.success(f"Хендлер {handlers[0].handler.__name__} сработал на сообщение.")
        print()
