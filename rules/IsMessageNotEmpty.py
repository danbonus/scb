from vkbottle_overrides.bot import rules, Message, SCB


class IsMessageNotEmpty(rules.ABCMessageRule):
    def __init__(self, nothing=None):
        pass

    async def check(self, message: Message, scb: SCB) -> bool:
        if message.text:
            return True
