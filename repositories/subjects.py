from logger import logger
from vkbottle_overrides.dispatch.rules.bot import LevensteinRule
from repositories.repository import Repository
from repositories.grades import GradesRepository
from repositories.user import UserRepository
from models.subject import SingleSubject
import re
import pymorphy2
from transliterate import translit

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
            print(name)
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

        for i in self.list_:
            if i.label in self.grades.subjects:
                grade_subjects.append(i)

        return grade_subjects

    async def list_func(self):
        subjects_list = []
        subjects_list.extend(self.phrases.subjects.default)
        subjects_from_db = await self.get()
        subjects_list.extend(subjects_from_db)
        logger.warning(subjects_from_db)
        return subjects_list

    def dict(self):  # доступ по лейблу из колбасок
        subjects = {}
        for subject in self.list_:
            subjects[subject.label] = subject
        return subjects

    def __contains__(self, item):
        if item in self.list_:
            return True

    def __getitem__(self, key):
        return self.dict[key]
# strip, lower и прочее в репозиториях
    async def is_subject(self, message):
        for i in self.list_:
            if await LevensteinRule(i.shorts).check(message):
                return i
