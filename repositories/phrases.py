import inspect
from jinja2 import Template
from languages import DefaultLanguage, languages

'''class Language:
    def __init__(self, lang_name):
        self.name = lang_name
        self.phrases = None

    def init(self):
        self.phrases = [i for i in dir(self) if not i.startswith("_")]
        for i in ["init", "name", "phrases"]:
            self.phrases.remove(i)
        return self.phrases'''


class PhrasesRepository(DefaultLanguage):
    """(message.client_info.button_actions[0].value
    Короче блять если нужны будут button_actions доделай эту хуйню вот тебе сниппет. Щас я не ебу юзабилити есть или
    нет у этой хуйни
    TODO: REFACTOR"""

    def __init__(self, name=None, client_info=None):
        for language in languages:
            if language().__name__ == name:
                self._language = language

                for section in self._language:
                    section_class = getattr(language, section)
                    self._section = section_class
                    setattr(self, section, section_class)

                    for phrase in self._section:
                        value = getattr(section_class, phrase)

                        if type(value) == dict:
                            priority_interaction_method = list(value.keys())[1]
                            if getattr(client_info, priority_interaction_method):
                                value = value[priority_interaction_method]
                            else:
                                value = value["plain"]

                        setattr(section_class, phrase, value)

    @property
    def _language(self):
        return [i for i in dir(self.__language) if not i.startswith("_")]

    @_language.setter
    def _language(self, value):
        self.__language = value

    @property
    def _section(self):
        return [i for i in dir(self.__section) if not i.startswith("_")]

    @_section.setter
    def _section(self, value):
        self.__section = value
