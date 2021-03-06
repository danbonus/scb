from vkbottle_overrides.bot import rules, Message, SCB


class NotRegistered(rules.ABCMessageRule):
    def __init__(self, nothing):
        pass

    async def check(self, message: Message, scb: SCB) -> bool:
        if not scb.user.registered:
            return True
