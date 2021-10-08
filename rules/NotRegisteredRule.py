from vkbottle.bot import rules, Message

from repositories.user import UserRepository


class NotRegisteredRule(rules.ABCMessageRule):
    async def check(self, message: Message) -> bool:
        user = await UserRepository(message.from_id)
        if not user.registered:
            return True
