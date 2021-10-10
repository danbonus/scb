from abc import ABC
from typing import Optional, Any, List, Callable

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle_overrides.dispatch.handlers.from_func_handler import ABCHandler
from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware
from vkbottle.dispatch.middlewares import BaseMiddleware, MiddlewareResponse
from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from logger import logger
from vkbottle.tools.dev_tools import message_min
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle_types.events import GroupEventType
from vkbottle import ABCDispenseView

from utils.args_object import SCB

DEFAULT_STATE_KEY = "peer_id"


class ABCMessageView(ABCDispenseView, ABC):
    def __init__(self):
        self.state_source_key = DEFAULT_STATE_KEY
        self.handlers: List["ABCHandler"] = []
        self.middlewares: List["BaseMiddleware"] = []
        self.default_text_approximators: List[Callable[[MessageMin], str]] = []
        self.handler_return_manager = BotMessageReturnHandler()

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(event["type"]) == GroupEventType.MESSAGE_NEW

    async def handle_event(
        self, event: dict, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:

        # logger.debug("Handling event ({}) with message view".format(event.get("event_id")))
        context_variables = {}
        message = message_min(event, ctx_api)
        message.state_peer = await state_dispenser.cast(self.get_state_key(event))
        scb = await SCB(message.from_id, message.client_info)

        for text_ax in self.default_text_approximators:
            message.text = text_ax(message)

        for middleware in self.middlewares:
            response = await middleware.pre(message, scb)
            if response == MiddlewareResponse(False):
                return
            elif isinstance(response, dict):
                context_variables.update(response)

        handle_responses = []
        handlers = []

        for handler in self.handlers:
            result = await handler.filter(message, scb)
            # logger.debug("Handler {} returned {}".format(handler, result))

            if result is False:
                continue

            elif isinstance(result, dict):
                context_variables.update(result)

            scb.context.update(context_variables)

            handler_response = await handler.handle(message, scb)
            handle_responses.append(handler_response)
            handlers.append(handler)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager, handler_response, message, context_variables
                )

            if handler.blocking:
                break

        for middleware in self.middlewares:
            await middleware.post(message, self, handle_responses, handlers)


class MessageView(ABCMessageView):
    def get_state_key(self, event: dict) -> Optional[int]:
        return event["object"]["message"].get(self.state_source_key)
