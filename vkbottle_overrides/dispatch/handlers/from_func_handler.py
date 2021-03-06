from typing import Any, Union
from typing import Callable

from vkbottle_overrides.dispatch.rules.abc import ABCRule
from .abc import ABCHandler


class FromFuncHandler(ABCHandler):
    def __init__(self, handler: Callable, *rules: "ABCRule", blocking: bool = True):
        self.handler = handler
        self.rules = rules
        self.blocking = blocking

    async def filter(self, event: Any, scb) -> Union[dict, bool]:
        rule_context = {}
        rules_passed = []

        for rule in self.rules:
            #print(rule)
            result = await rule.check(event, scb)
            #print(result)
            if result is False or result is None:
                return False
            elif result is True:
                rules_passed.append(rule)
                continue
            #print(result
             #     )
            #print(rule)
            rule_context.update(result)

        return rule_context

    async def handle(self, event: Any, scb, **context) -> Any:
        return await self.handler(event, scb, **context)

    def __repr__(self):
        return f"<FromFuncHandler {self.handler.__name__} blocking={self.blocking} rules={self.rules}>"
