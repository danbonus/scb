from repositories import user, phrases, grades, many_users, subjects  # CIRCULAR IMPORT ERROR !!!
from models import subject
from utils.api import Api
from utils.my_time import MyTime
from vkbottle_overrides.tools import CtxStorage
from . import AsyncObject


class SCB(AsyncObject):
    async def __init__(self, event, context):
        self.context = context
        self.user: user.UserRepository = await user.UserRepository(event.object.user_id)
        #new_request_id = await requests.RequestsRepository.create(message, context["event"])
        #self.requests: requests.RequestsRepository = await requests.RequestsRepository(request_id=new_request_id)
        self.storage: CtxStorage = CtxStorage(section=self.user.uid)
        self.phrases: phrases.PhrasesRepository = phrases.PhrasesRepository(
            self.user,
            None
        )
        self.grades: grades.GradesRepository = await grades.GradesRepository(self.user.grade)
        self.subjects: subjects.SubjectsRepository = await subjects.SubjectsRepository(
            self.phrases, self.grades, self.user
        )
        self.single_subject = subject.SingleSubject
        self.many_users: many_users.ManyUsersRepository = many_users.ManyUsersRepository()
        self.api: Api = Api()
        self.time = MyTime()

        self.storage.set("SCB", self)
        self.rule_toggled = None
