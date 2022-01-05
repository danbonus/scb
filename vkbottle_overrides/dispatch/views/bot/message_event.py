from abc import ABC
from typing import Optional, Any, List, Callable
from vkbottle import ABCDispenseView
from vkbottle import GroupTypes
from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle.dispatch.middlewares import BaseMiddleware, MiddlewareResponse
from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle_types.events import GroupEventType
from vkbottle_types.state import StatePeer

from logger import logger
from utils.args_object import SCB
from vkbottle_overrides.dispatch.handlers.from_func_handler import ABCHandler
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware

DEFAULT_STATE_KEY = "peer_id"


class MessageEvent(GroupTypes.MessageEvent):
    state_peer: Optional[StatePeer] = None


class ABCMessageEventView(ABCDispenseView, ABC):
    def __init__(self):
        self.state_source_key = DEFAULT_STATE_KEY
        self.handlers: List["ABCHandler"] = []
        self.states = {}
        self.middlewares: List["BaseMiddleware"] = []
        self.default_text_approximators: List[Callable[[MessageMin], str]] = []
        self.handler_return_manager = BotMessageReturnHandler()

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(event["type"]) == GroupEventType.MESSAGE_EVENT

    async def handle_event(
        self, event: dict, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:
        # logger.debug("Handling event ({}) with message view".format(event.get("event_id")))
        context_variables = {}

        event = MessageEvent(**event)

        event.unprepared_ctx_api = ctx_api
        event.state_peer = await state_dispenser.cast(self.get_state_key(event))
        #print(event.state_peer)
        #setattr(event, "state_peer", await state_dispenser.cast(self.get_state_key(event)))

        scb = await SCB(event, {"event": event, "handlers": self.handlers, "states": self.states})

        for middleware in self.middlewares:
            response = await middleware.pre(event, scb)
            if response == MiddlewareResponse(False):
                return
            elif isinstance(response, dict):
                context_variables.update(response)

        handle_responses = []
        handlers = []

        for handler in self.handlers:
            result = await handler.filter(event, scb)
            logger.spam("Handler {} returned {}".format(handler, result))

            if result is False:
                continue

            elif isinstance(result, dict):
                context_variables.update(result)

            scb.context.update(context_variables)
            #print(context_variables)
            #print(handler)
            handler_response = await handler.handle(event, scb, **context_variables)
            handle_responses.append(handler_response)
            handlers.append(handler)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager, handler_response, event, context_variables
                )

            if handler.blocking:
                break
            event.state_peer = await state_dispenser.cast(self.get_state_key(event))

        for middleware in self.middlewares:
            await middleware.post(event, self, handle_responses, handlers, scb)


class MessageEventView(ABCMessageEventView):
    def get_state_key(self, event: MessageEvent) -> Optional[int]:
        print(self.state_source_key)
        return event.object.peer_id
