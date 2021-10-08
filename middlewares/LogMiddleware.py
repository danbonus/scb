from vkbottle import BaseMiddleware, MiddlewareResponse, ABCView
from logger import logger
from repositories.user import UserRepository
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from vkbottle.bot import Message
from typing import List, Any

from vkbottle_overrides import ABCHandler


class LogMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin):
        pass

    async def post(
            self,
            message: Message,
            view: "ABCView",
            handle_responses: List[Any],
            handlers: List["ABCHandler"],
    ):
        if not handlers:
            return

        print(f"{len(handlers)} хендлеров сработало на сообщение. "
              f"Они вернули {handle_responses}, "
              f"все они принадлежали к view {view}")