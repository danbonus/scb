from vkbottle import ABCView
from logger import logger
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from vkbottle_overrides.bot import Message
from typing import List, Any
from utils.args_object import SCB

from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


class DebugMiddleware(BaseMiddleware):
    async def post(
            self,
            message: Message,
            view: "ABCView",
            handle_responses: List[Any],
            handlers: List["FromFuncHandler"],
            scb: SCB
    ):
        msg = "⚠️ | Дебаг-отчёт:\n"
        msg += "Ваше сообщение: %s\n" % message.text
        if message.state_peer:
            msg += "Созданный стейт: %s\n" % message.state_peer.state
            msg += "Дерево стейтов: %s" % ', '.join([f"{i}: {message.state_peer.tree[i]['handler'].handler.__name__ if message.state_peer.tree[i]['handler'] else 'None' }" for i in message.state_peer.tree])
        else:
            msg += "Стейта нет.\n"

        await message.answer(msg)