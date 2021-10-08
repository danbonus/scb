from typing import Set, Tuple, Union

from vkbottle.bot import BotLabeler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views import RawEventView
from vkbottle.tools.dev_tools.utils import convert_shorten_filter
from vkbottle_overrides import MessageView, FromFuncHandler
from vkbottle.framework.bot.labeler.abc import LabeledMessageHandler

ShortenRule = Union[ABCRule, Tuple[ABCRule, ...], Set[ABCRule]]


class SCBLabeler(BotLabeler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_view = MessageView()
        self.raw_event_view = RawEventView()

    def message(
        self, *rules: ShortenRule, blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    *map(convert_shorten_filter, rules),
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

