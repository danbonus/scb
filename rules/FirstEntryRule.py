from vkbottle.bot import rules, Message

from logger import logger
from repositories.user import UserRepository


class FirstEntryRule(rules.ABCMessageRule):
    def __init__(self, nothing):
        pass

    async def check(self, message: Message) -> bool:
        #logger.debug("Checking for first entry")
        user = await UserRepository(message.from_id)
        #print(user.newbie)
        if user.newbie:
            logger.debug("Newbie!!")
            return True
