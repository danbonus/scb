from typing import List, Any
from vkbottle import ABCView
from vkbottle import GroupTypes

from utils.args_object import SCB
from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


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
