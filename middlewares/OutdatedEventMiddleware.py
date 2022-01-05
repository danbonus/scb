import json

from vkbottle import GroupTypes
from vkbottle import MiddlewareResponse

from logger import logger
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


class OutdatedEventMiddleware(BaseMiddleware):
    async def pre(self, event: GroupTypes.MessageEvent, scb):
        if "message_ids" not in scb.storage:
            await event.unprepared_ctx_api.messages.send_message_event_answer(
                event_id=event.object.event_id,
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                event_data=json.dumps(
                    {
                        "type": "show_snackbar",
                        "text": "Просрочено! Упс."
                    }
                )
            )
            return MiddlewareResponse(False)
        logger.debug("Event is not outdated.")