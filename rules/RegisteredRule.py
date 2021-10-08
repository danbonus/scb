from vkbottle.bot import rules, Message

from repositories.user import UserRepository


class RegisteredRule(rules.ABCMessageRule):
    async def check(self, message: Message) -> bool:
        user = await UserRepository(message.from_id)
        if user.registered:
            return True
