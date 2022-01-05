from .homework_record import HomeworkRecord
from .schedule_element import ScheduleElement


class Lesson:
    def __init__(self, homework: HomeworkRecord, schedule_element: ScheduleElement):
        self.room = schedule_element.room
        self.bell = schedule_element.bell
        self.subject = schedule_element.subject
        self.homework = homework
        self.replace = schedule_element.replace
