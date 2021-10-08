from vkbottle_overrides.bot import rules, Message, SCB

from logger import logger
from repositories.user import UserRepository


class FirstEntry(rules.ABCMessageRule):
    def __init__(self, nothing):
        pass

    async def check(self, message: Message, scb: SCB) -> bool:
        if scb.user.newbie:
            logger.debug("Newbie!!")
            return True
