from repositories import user, phrases, grades, many_users  # CIRCULAR IMPORT ERROR !!!
from vkbottle import CtxStorage
from . import AsyncObject


class SCB(AsyncObject):
    async def __init__(self, uid, client_info):
        self.storage: CtxStorage = CtxStorage()
        self.user: user.UserRepository = await user.UserRepository(uid)
        self.phrases: phrases.PhrasesRepository = phrases.PhrasesRepository(self.user.lang, client_info)
        self.grades = grades.GradesRepository
        self.many_users: many_users.ManyUsersRepository = many_users.ManyUsersRepository()
        self.context = {}
        self.rule_toggled = None
