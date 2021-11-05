from vkbottle_overrides.bot import rules, Message, SCB


class IsAdmin(rules.ABCMessageRule):
    def __init__(self, nothing=None):
        pass

    async def check(self, message: Message, scb: SCB) -> bool:
        if scb.user.is_admin:
            return True
