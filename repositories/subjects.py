import pymorphy2
import re
from transliterate import translit

from logger import logger
from models.subject import SingleSubject
from repositories.grades import GradesRepository
from repositories.repository import Repository
from repositories.user import UserRepository
from vkbottle_overrides.dispatch.rules.bot import LevensteinRule


class SubjectsRepository(Repository):
    async def __init__(self, phrases, grades: GradesRepository, user: UserRepository):
        super().__init__("subjects")
        self.grades = grades
        self.phrases = phrases
        self.user = user
        self.list_ = await self.list_func()
        self.dict = self.dict()
        self.yesterday = ...
        self.current_day = ...
        self.tomorrow_day = ...

    async def create(self, **info):
        pattern = re.compile('[\W_]+')
        label = pattern.sub('', info["label"]).lower()
        label = translit(label, "ru", reversed=True)

        cases = {}
        name = info["name"]
        is_russian = re.compile(r'[а-яА-ЯёЁ]')

        if is_russian.match(name):
            morph = pymorphy2.MorphAnalyzer()
            subject = morph.parse(label)
            cases["nomn"] = subject[0].inflect({"nomn"}).word.capitalize().strip()

            for i in ["gent", "datv", "accs", "ablt", "loct"]:
                cases[i] = subject[0].inflect({i}).word.lower().strip()
        else:
            cases["nomn"] = name.capitalize()
            for i in ["gent", "datv", "accs", "ablt", "loct"]:
                cases[i] = name.lower().strip()

        record = {
                "label": label.strip(),
                "cases": cases,
                "shorts": info["shorts"],
                "emoji": info["emoji"]
            }
        self._db.insert_one(record)
        return record

    async def _get_record(self):
        self._db.find_one()
    #  подумать над оптимизацией кода (проперти и тп, чтобы лишний раз не вызывать код)
    async def get(self):
        records = self._db.find({})
        #subjects = {}

        #for i in records:
        #    subjects[i["label"]] = SingleSubject(i)
        #print(#)
        return [SingleSubject(i) async for i in records]

    async def update(self, **info):
        ...

    async def delete(self):
        ...

    @property
    def grades_subjects(self):
        grade_subjects = []

        logger.debug(self.list_)
        for i in self.list_:
            if i.label in self.grades.subjects:
                grade_subjects.append(i)
        logger.debug(grade_subjects)
        return grade_subjects

    async def list_func(self):
        subjects_list = []
        subjects_list.extend(self.phrases.subjects.default)
        subjects_from_db = await self.get()
        subjects_list.extend(subjects_from_db)
        #logger.warning(subjects_from_db)
        return subjects_list

    def dict(self):  # доступ по лейблу из колбасок
        subjects = {}
        for subject in self.list_:
            subjects[subject.label] = subject
        return subjects

    async def is_subject(self, message):
        for i in self.list_:
            if await LevensteinRule(i.shorts).check(message):
                return i

    async def find_groups(self, subject):
        groups = self.grades.lang_groups
        groups.extend(self.grades.exam_groups)
        logger.debug(subject)
        if subject[-1].isdigit():
            subject = subject[:-1]

        for group in groups:
            subjects_count = len(group.subjects)
            for group_subject in group.subjects:
                if subject == group_subject[:-1]:
                    return [self.dict[subject + str(i+1)] for i in range(subjects_count)]

        logger.debug(subject)
        #print([i.label for i in self.list_ if subject in i.label])
        #groups = len([i.label for i in self.list_ if i.label.startswith(subject)]) - 1
        logger.debug(groups)
        #return [self.dict[subject + str(i+1)] for i in range(groups)]

    def __contains__(self, item):
        if item in self.list_:
            return True

    def __getitem__(self, key):
        return self.dict[key]
    # strip, lower и прочее в репозиториях
