from typing import Set, Tuple, Union
import re
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union
from vkbottle.bot import BotLabeler
from vkbottle_overrides.dispatch.rules.abc import ABCRule
from vkbottle_overrides.tools.dev_tools.utils import convert_shorten_filter
from vkbottle_overrides.dispatch.views.bot import MessageView
from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle.framework.bot.labeler.abc import LabeledMessageHandler
import vbml

from vkbottle_overrides.dispatch.rules.bot import (
    AttachmentTypeRule,
    ChatActionRule,
    CommandRule,
    CoroutineRule,
    FromPeerRule,
    FromUserRule,
    FuncRule,
    LevensteinRule,
    MessageLengthRule,
    PayloadContainsRule,
    PayloadMapRule,
    PayloadRule,
    PeerRule,
    RegexRule,
    StateGroupRule,
    StateRule,
    StickerRule,
    MacroRule,
    VBMLRule,
)

ShortenRule = Union[ABCRule, Tuple[ABCRule, ...], Set[ABCRule]]
DEFAULT_CUSTOM_RULES: Dict[str, Type[ABCRule]] = {
    "from_chat": PeerRule,
    "command": CommandRule,
    "from_user": FromUserRule,
    "peer_ids": FromPeerRule,
    "sticker": StickerRule,
    "attachment": AttachmentTypeRule,
    "levenstein": LevensteinRule,
    "lev": LevensteinRule,
    "length": MessageLengthRule,
    "action": ChatActionRule,
    "payload": PayloadRule,
    "payload_contains": PayloadContainsRule,
    "payload_map": PayloadMapRule,
    "func": FuncRule,
    "coro": CoroutineRule,
    "coroutine": CoroutineRule,
    "state": StateRule,
    "state_group": StateGroupRule,
    "regexp": RegexRule,
    "regex": RegexRule,
    "macro": MacroRule,
    "text": VBMLRule,
}


class SCBLabeler(BotLabeler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_view = MessageView()
        self.custom_rules = kwargs.get("custom_rules") or DEFAULT_CUSTOM_RULES
        self.rule_config: Dict[str, Any] = {
            "vbml_flags": re.MULTILINE | re.DOTALL,  # Flags for VBMLRule
            "vbml_patcher": vbml.Patcher(),  # Patcher for VBMLRule
        }

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
