from typing import Callable
from logger import logger

from abc import ABC, abstractmethod
from typing import Any, Union
from vkbottle_overrides.dispatch.rules.abc import ABCRule
from .abc import ABCHandler
import inspect
import os


class FromFuncHandler(ABCHandler):
    def __init__(self, handler: Callable, *rules: "ABCRule", blocking: bool = True):
        self.handler = handler
        self.rules = rules
        self.blocking = blocking

    async def filter(self, event: Any, scb) -> Union[dict, bool]:
        rule_context = {}
        rules_passed = []

        for rule in self.rules:
            result = await rule.check(event, scb)
            logger.debug(type(rule))
            logger.debug(result)

            if result is False or result is None:
                return False
            elif result is True:
                rules_passed.append(rule)
                continue
            rule_context.update(result)

        return rule_context

    async def handle(self, event: Any, scb) -> Any:
        return await self.handler(event, scb)

    def __repr__(self):
        return f"<FromFuncHandler {self.handler.__name__} blocking={self.blocking} rules={self.rules}>"
