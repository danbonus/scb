from vkbottle import ABCView
from logger import logger
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from vkbottle.bot import Message
from typing import List, Any
from utils.args_object import SCB

from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware
from vkbottle import GroupTypes


class EventAnswerMiddleware(BaseMiddleware):
    async def post(
            self,
            event: GroupTypes.MessageEvent,
            view: "ABCView",
            handle_responses: List[Any],
            handlers: List["FromFuncHandler"],
            scb: SCB
    ):
        await event.unprepared_ctx_api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.user_id
        )
