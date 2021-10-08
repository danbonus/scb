from vkbottle_overrides.bot import rules, Message, SCB

from repositories.user import UserRepository


class RegisteredRule(rules.ABCMessageRule):
    async def check(self, message: Message, scb: SCB) -> bool:
        if scb.user.registered:
            return True
