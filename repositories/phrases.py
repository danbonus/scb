from string import Template
from languages import DefaultLanguage, languages
from utils.my_time import my_time
from logger import logger


class PhrasesRepository(DefaultLanguage):
    """
    (message.client_info.button_actions[0].value
    Короче блять если нужны будут button_actions доделай эту хуйню вот тебе сниппет. Щас я не ебу юзабилити есть или
    нет у этой хуйни
    ЭТО ПОЛНЫЙ АНАЛ!!!!!!!!!!
    Пришлось создавать новый класс секций при каждой инициализации репозитория фраз, т.к., как ни странно,
    при изменении переменной не инстанса класса, а объекта меняется ее значение глобально. А это значит, что
    все мои темплейты заменяются на отформатированные жинжей2 строки. И следующие юзеры видят в сообщение не свое имя,
    а имя того, кто первее написал боту. Пиздец! Сила ООП.
    """

    def __init__(self, user, client_info):
        logger.spam("PHrases rep init")
        for language in languages:  # итерация по доступным языкам
            if language().__name__ == user.lang:  # !!! __name__ класса переопределено чтобы скрыть переменную в IDE
                for section_name in self._attributes(language):  # итерация по атрибутам языка (секциям)
                    section = getattr(language, section_name)  # объект секции
                    section = type(section_name, (section,), dict(section.__dict__))  # динамический объект сессии

                    setattr(self, section_name, section)  # переопределение объекта секции на динамический

                    for phrase in self._attributes(section):  # итерация по атрибутам секции (фразам)
                        value = getattr(section, phrase)  # фраза

                        if type(value) == dict:  # если у фразы есть несколько вариантов взаимодействия с юзером
                            priority_interaction_method = list(value.keys())[1]  # второй ключ словаря приориретнее

                            if hasattr(client_info, priority_interaction_method):  # если у юзера есть кнопки, например
                                value = value[priority_interaction_method]
                            else:
                                value = value["plain"]  # обычный текст, использование кнопок и тд не предусматривается

                        if type(value) == Template:  # если есть форматирование
                            if user.last_request.timestamp + 18000 < my_time.now.timestamp():  # нужно ли приветствовать
                                value = value.safe_substitute(
                                        greeting=language.__greetings__[my_time.time_of_day()] % user.first_name
                                    )
                                if Template.pattern.findall(value):
                                    value = Template(value)
                            else:
                                value = value.safe_substitute(greeting="")

                        setattr(section, phrase, value)  # присвоение выбранной фразы динамическому объекту секции

    @staticmethod
    def _attributes(obj):
        return [i for i in dir(obj) if not i.startswith("_")]  # исключение приватных переменных
