from vkbottle.bot import Message

from repositories import (
    user,
    phrases,
    grades,
    many_users,
    requests,
    subjects,
    schedule,
    homework,
    time,
    replaces
)
# CIRCULAR IMPORT ERROR !!!
from utils import api, utils
from vkbottle_overrides.tools import CtxStorage
from . import AsyncObject


class SCB(AsyncObject):
    async def __init__(self, event, context=None):
        #print(event)
        if isinstance(event, Message):
            self.from_id = event.from_id
            self.client_info = event.client_info
            self.text = event.text
            self.date = event.date
            self.state_peer = event.state_peer
            self.context_event = context["event"] if context else None

            create_request = True
        elif isinstance(event, dict):
            self.from_id = event["user_id"]
            self.text = event["text"]
            self.date = event["date"]
            self.state_peer = None
            self.context_event = None

            create_request = True

            self.client_info = None
        else:
            self.from_id = event.object.user_id
            self.client_info = None
            create_request = False

        self.user: user.UserRepository = await user.UserRepository(self.from_id)
        self.storage: CtxStorage = CtxStorage(section=self.user.uid)
        self.time: time.TimeRepository = time.TimeRepository(self.storage)
        self.phrases: phrases.PhrasesRepository = phrases.PhrasesRepository(self.user, self.client_info, self.time)

        if create_request:
            new_request_id = await requests.RequestsRepository.create(
                self.from_id,
                self.text,
                self.date,
                self.state_peer,
                self.context_event
            )
            self.requests: requests.RequestsRepository = await requests.RequestsRepository(request_id=new_request_id)

        self.grades: grades.GradesRepository = await grades.GradesRepository(self.user.grade)
        self.subjects: subjects.SubjectsRepository = await subjects.SubjectsRepository(self.phrases, self.grades, self.user)
        self.many_users: many_users.ManyUsersRepository = many_users.ManyUsersRepository()

        self.api: api.Api = api.Api()

        if self.user.registered:
            self.replaces: replaces.ReplacesRepository = await replaces.ReplacesRepository(self.grades, self.subjects,
                                                                                           self.time)
            self.schedule: schedule.ScheduleRepository = await schedule.ScheduleRepository(self.grades, self.subjects, self.time)
            self.homework: homework.HomeworkRepository = await homework.HomeworkRepository(self.schedule, self.time, self.api, self.user, self.replaces, self.grades.homework_db)

        self.utils = utils
        self.context = context

        self.storage.set("SCB", self)
