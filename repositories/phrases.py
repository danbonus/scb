import inspect
from jinja2 import Template


'''class Language:
    def __init__(self, lang_name):
        self.name = lang_name
        self.phrases = None

    def init(self):
        self.phrases = [i for i in dir(self) if not i.startswith("_")]
        for i in ["init", "name", "phrases"]:
            self.phrases.remove(i)
        return self.phrases'''


class DefaultLanguageFields:
    _name = "normal"
    greeting = "Привет!"
    first_entry = {
        "plain": "Привет! Ты тут в первый раз. Отправь цифру 1, чтобы зарегистрироваться.",
        "keyboard": "Привет! Ты тут в первый раз. Нажми кнопку, чтобы начать регистрацию."
    }
    must_register = {
        "plain": "Нужно зарегистрироваться! Отправь цифру 1 или напиши <<Пройти регистрацию>>",
        "keyboard": "Жми на кнопку и регистрируйся!"
    }
    reg_grade = {
        "plain": "Для начала выбери свой класс из списка: ",
        "keyboard": "Для начала выбери свой класс."
    }

    wrong_grade = "Такого класса нет. Выбери из списка."
    broadcast = {
        "plain": "Твой класс: %s. \nВ боте есть рассылка беу беу. Напиши <<да>> или <<нет>>.",
        "keyboard": "Твой класс: %s. \nВ боте есть рассылка беу беу. Включить?"
    }

    broadcast_not_stated = "И что это за хуйня? Да или нет, ясно же должно быть."

    broadcast_type = {
        "plain": "У рассылки есть два типа: \n"
                 "1) ДЗ будет приходить, например, через час с конца последнего урока. Удобно.\n"
                 "2) Независимо от расписания, в указанное время. И в понедельник в 16, и в субботу в 16. "
                 "Old-fashioned way.\n\n"
                 "Напиши цифру 1 или 2, чтобы выбрать тип рассылки.",

        "keyboard": "У рассылки есть два типа: \n"
                    "1) ДЗ будет приходить, например, через час с конца последнего урока. Удобно.\n"
                    "2) Независимо от расписания, в указанное время. И в понедельник в 16, и в субботу в 16. "
                    "Old-fashioned way.\n\n"
                    "Нажми на кнопку, чтобы выбрать."

    }

    broadcast_time_since = {
        "plain": "Стандартное время с конца урока до начала рассылки -- 1 час. Можешь поменять на свое "
                 "(формат часы:минуты).\nНапример: 00:30 -- придет через полчаса после конца уроков, а 01:00 -- через час.",
        "keyboard": "Стандартное время с конца урока до начала рассылки -- 1 час. Можешь выбрать другое в панели или "
                    "поменять на свое (формат часы:минуты). Например: 00:30 -- придет через полчаса после конца уроков, "
                    "а 01:00 -- через час."
    }

    broadcast_time_fixed = {
        "plain": "Стандартное время рассылки -- 16:00. \nЧтобы оставить его, напиши 1."
                 "Также время можно поменять на своё: отправь его в "
                 "формате часы:минуты.",
        "keyboard": "Стандартное время рассылки -- 16:00. \n    Выбери время в панели, либо напиши удобное время текстом."
    }

    broadcast_wrong_format = "Неверный формат времени."
    registration_passed = Template("Регистрация пройдена. \nТвой класс: {{grade}}.\nПодписан на рассылку: {{result}}.")


class PhrasesRepository(DefaultLanguageFields):
    """(message.client_info.button_actions[0].value
    Короче блять если нужны будут button_actions доделай эту хуйню вот тебе сниппет. Щас я не ебу юзабилити есть или
    нет у этой хуйни"""

    def __init__(self, name=None, client_info=None):
        for language in available_languages:
            if language._name == name:
                for phrase in [i for i in dir(language) if not i.startswith("_")]:
                    value = getattr(language, phrase)

                    if type(value) == dict:
                        priority_interaction_method = list(value.keys())[1]
                        if getattr(client_info, priority_interaction_method):
                            value = value[priority_interaction_method]
                        else:
                            value = value["plain"]

                    setattr(self, phrase, value)


'''gachi_language = Language("gachi")
gachi_language.greeting = "Hey leatherman"
gachi_language.first_entry = "♂️ ATTENTION! ♂️ I see you there first time, ♂️ fucking slave ♂️!"
gachi_language.beu = "!!!"'''

available_languages = [
    DefaultLanguageFields
]
