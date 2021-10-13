from repositories import user, phrases, grades, many_users, requests  # CIRCULAR IMPORT ERROR !!!
from vkbottle import CtxStorage
from . import AsyncObject


class SCB(AsyncObject):
    async def __init__(self, message):
        self.storage: CtxStorage = CtxStorage()
        self.user: user.UserRepository = await user.UserRepository(message.from_id)
        self.phrases: phrases.PhrasesRepository = phrases.PhrasesRepository(
            self.user,
            message.client_info
        )
        self.grades: grades.GradesRepository = await grades.GradesRepository()
        self.many_users: many_users.ManyUsersRepository = many_users.ManyUsersRepository()
        self.requests: requests.RequestsRepository = await requests.RequestsRepository()
        self.storage.set("SCB", self)
        self.context = {}
        self.rule_toggled = None
