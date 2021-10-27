from repositories.repository import Repository
from repositories.grades import GradesRepository
from repositories.subjects import SubjectsRepository
from utils.my_time import MyTime
from models.schedule_element import ScheduleElement


class ScheduleRepository(Repository):
    async def __init__(self, grades: GradesRepository, subjects: SubjectsRepository, time: MyTime):
        super().__init__("schedule")
        self.grades = grades
        self.subjects = subjects
        self.time = time
        self.bells_time = {
            0: ["8:05", "8:50"],
            1: ["9:00", "9:45"],
            2: ["10:05", "10:50"],
            3: ["11:10", "11:55"],
            4: ["12:10", "12:55"],
            5: ["13:10", "13:55"],
            6: ["14:10", "14:55"],
            7: ["15:05", "15:50"]
        }
        self.schedule = grades.schedule
        this_day, tomorrow_day = time.check_for_weekday()
        today_schedule = self.schedule[str(this_day.weekday())]
        tomorrow_schedule = self.schedule[str(tomorrow_day.weekday())]
        start_ts, end_ts = time.start_end(this_day)

        print(today_schedule)

        self.today = [ScheduleElement(subjects, value) for key, value in today_schedule.items()]
        self.tomorrow = [ScheduleElement(subjects, value) for key, value in tomorrow_schedule.items()]

    '''async def create(self, **info ):
        model = {
            "monday": ...,
            "tuesday": ...,
            "wednesday": ...,
            "thursday": ...,
            "friday": ...,
            "saturday": ...,
            "sunday": ...
        }
        await self.grades.update(schedule=model)'''

    async def _get_record(self):
        self._db.find_one()

    @staticmethod
    async def get(name):
        ...

    async def update(self, **info):
        ...

    async def delete(self):
        ...

    @property
    async def list(self):
        return

    def dict(self):  # доступ по лейблу из колбасок
        subjects = {}
        for subject in self.list_:
            subjects[subject.label] = subject
        return subjects

    def __getitem__(self, key):
        return self.dict[key]