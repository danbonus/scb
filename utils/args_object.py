from repositories import (
    user,
    phrases,
    grades,
    many_users,
    requests,
    subjects,
    schedule,
    homework
) # CIRCULAR IMPORT ERROR !!!
from models import subject
from utils.api import Api
from utils.my_time import MyTime
from vkbottle_overrides.tools import CtxStorage
from . import AsyncObject


class SCB(AsyncObject):
    async def __init__(self, message, context):
        self.context = context
        self.user: user.UserRepository = await user.UserRepository(message.from_id)
        new_request_id = await requests.RequestsRepository.create(message, context["event"])
        self.requests: requests.RequestsRepository = await requests.RequestsRepository(request_id=new_request_id)
        self.storage: CtxStorage = CtxStorage(section=self.user.uid)
        self.phrases: phrases.PhrasesRepository = phrases.PhrasesRepository(
            self.user,
            message.client_info
        )
        self.grades: grades.GradesRepository = await grades.GradesRepository(self.user.grade)
        self.subjects: subjects.SubjectsRepository = await subjects.SubjectsRepository(
            self.phrases, self.grades, self.user
        )
        self.single_subject = subject.SingleSubject
        self.many_users: many_users.ManyUsersRepository = many_users.ManyUsersRepository()
        self.api: Api = Api()
        self.time = MyTime()
        if self.user.registered:
            self.schedule: schedule.ScheduleRepository = await schedule.ScheduleRepository(self.grades, self.subjects, self.time)
            self.homework: homework.HomeworkRepository = await homework.HomeworkRepository(self.schedule, self.time, self.grades.homework_db)
        self.storage.set("SCB", self)
        self.rule_toggled = None
