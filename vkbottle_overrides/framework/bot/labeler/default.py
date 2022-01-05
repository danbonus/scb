import re
import vbml
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union
from vkbottle.bot import BotLabeler
from vkbottle.dispatch.views import ABCView
from vkbottle_types.events import GroupEventType

from logger import logger
from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle_overrides.dispatch.rules.abc import ABCRule
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
from vkbottle_overrides.dispatch.views import HandlerBasement, MessageView, RawEventView, MessageEventView
from vkbottle_overrides.tools.dev_tools.utils import convert_shorten_filter
from .abc import LabeledHandler, LabeledMessageHandler, EventName

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
        self.message_event_view = MessageEventView()
        self.raw_event_view = RawEventView()
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
            #print(custom_rules)
            if not func.__name__.startswith("back"):
                if 'state' in custom_rules:
                    if not isinstance(custom_rules['state'], list):
                        custom_rules['state'] = [custom_rules['state']]
                    for i in custom_rules['state']:
                        if i in self.message_view.states:
                            self.message_view.states[i].append(func.__name__)
                        else:
                            self.message_view.states[i] = [func.__name__]
                else:
                    if "NO_STATE" in self.message_view.states:
                        self.message_view.states["NO_STATE"].append(func.__name__)
                    else:
                        self.message_view.states["NO_STATE"] = [func.__name__]
            return func

        return decorator

    def private_message(
        self, *rules: ShortenRule, blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    PeerRule(False),
                    *map(convert_shorten_filter, rules),
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            if not func.__name__.startswith("back"):
                if 'state' in custom_rules:
                    if not isinstance(custom_rules['state'], list):
                        custom_rules['state'] = [custom_rules['state']]
                    for i in custom_rules['state']:
                        if i in self.message_view.states:
                            self.message_view.states[i].append(func.__name__)
                        else:
                            self.message_view.states[i] = [func.__name__]
                else:
                    if "NO_STATE" in self.message_view.states:
                        self.message_view.states["NO_STATE"].append(func.__name__)
                    else:
                        self.message_view.states["NO_STATE"] = [func.__name__]
            return func

        return decorator

    def raw_event(
        self,
        event: Union[EventName, List[EventName]],
        dataclass: Callable = dict,
        *rules: ShortenRule,
        **custom_rules,
    ) -> LabeledHandler:

        if not isinstance(event, list):
            event = [event]

        def decorator(func):
            for e in event:

                if isinstance(e, str):
                    e = GroupEventType(e)

                self.raw_event_view.handlers[e] = HandlerBasement(
                    dataclass,
                    FromFuncHandler(
                        func,
                        *map(convert_shorten_filter, rules),
                        *self.auto_rules,
                        *self.get_custom_rules(custom_rules),
                    ),
                )
            return func

        return decorator

    def message_event(self, *rules: ShortenRule, blocking: bool = True, **custom_rules) -> LabeledMessageHandler:
        def decorator(func):
            self.message_event_view.handlers.append(
                FromFuncHandler(
                    func,
                    *map(convert_shorten_filter, rules),
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            #print(custom_rules)
            if not func.__name__.startswith("back"):
                if 'state' in custom_rules:
                    if not isinstance(custom_rules['state'], list):
                        custom_rules['state'] = [custom_rules['state']]
                    for i in custom_rules['state']:
                        if i in self.message_event_view.states:
                            self.message_event_view.states[i].append(func.__name__)
                        else:
                            self.message_event_view.states[i] = [func.__name__]
                else:
                    self.message_event_view.states["NO_STATE"] = [func.__name__]

            return func

        return decorator

    def load(self, labeler: "SCBLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        for state, handlers in labeler.message_view.states.items():
            if state in self.message_view.states:
                logger.critical("State %s in view" % state)
                logger.critical("Handlers: %s" % handlers)
                self.message_view.states[state].extend(handlers)
            else:
                logger.critical("State %s not in view" % state)
                logger.critical("Handlers: %s" % handlers)
                self.message_view.states[state] = handlers

        self.message_view.middlewares.extend(labeler.message_view.middlewares)
        self.message_event_view.handlers.extend(labeler.message_event_view.handlers)
        self.message_event_view.middlewares.extend(labeler.message_event_view.middlewares)
        self.raw_event_view.handlers.update(labeler.raw_event_view.handlers)
        self.raw_event_view.middlewares.extend(labeler.raw_event_view.middlewares)

    def views(self) -> Dict[str, "ABCView"]:
        return {
            "message": self.message_view,
            "message_event": self.message_event_view,
            "raw": self.raw_event_view
        }
