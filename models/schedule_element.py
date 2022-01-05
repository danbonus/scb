from repositories.subjects import SubjectsRepository
from .subject import SingleSubject


class ScheduleElement:
    def __init__(self, subjects: SubjectsRepository, schedule_element):
        self.subject: SingleSubject = subjects[schedule_element["subject"]]
        self.room = schedule_element["room"]
        self.bell = schedule_element["bell"]
        self.replace = None
