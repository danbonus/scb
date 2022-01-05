from typing import List

from models.schedule_element import ScheduleElement
from repositories.grades import GradesRepository
from repositories.repository import Repository
from repositories.subjects import SubjectsRepository
from repositories.time import TimeRepository


class ScheduleRepository(Repository):
    async def __init__(self, grades: GradesRepository, subjects: SubjectsRepository, time: TimeRepository):
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
        this_day, tomorrow_day = time.get_days_of_school()
        start_ts, end_ts = time.get_day_time_borders(this_day)

        self.schedule = {}
        for day, day_schedule in grades.schedule.items():
            self.schedule[day] = []
            for bell, element in day_schedule.items():
                self.schedule[day].append(ScheduleElement(subjects, element))

        #self.today = self.schedule[str(this_day.weekday())]
        #self.tomorrow = self.schedule[str(tomorrow_day.weekday())]


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

    def __getitem__(self, key) -> List[ScheduleElement]:
        return self.schedule[key]
