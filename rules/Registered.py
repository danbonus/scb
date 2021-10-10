from vkbottle_overrides.bot import rules, Message, SCB


class Registered(rules.ABCMessageRule):
    async def check(self, message: Message, scb: SCB) -> bool:
        if scb.user.registered:
            return True
