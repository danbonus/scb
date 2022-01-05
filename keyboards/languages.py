from vkbottle import Text

from vkbottle_overrides import Keyboard


def languages_iteration(languages_list):
    languages_plain = ""
    languages_keyboard = Keyboard()
    #  LANGUAGES_KEYBOARD.buttons = []

    for identifier, label in languages_list.items():
        languages_keyboard.add(Text(label, {"language": identifier}), row=3)
        languages_plain += f"-- {label}\n"

    return languages_plain, languages_keyboard
