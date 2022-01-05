from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard
from .misc import BACK_TO_MENU


def replaces_iteration(schedule):
    keyboard = Keyboard()
    for i in schedule:
        if i.subject.lang_group or i.subject.exam_group:
            label = f"{i.bell}. {i.subject.nomn}" + i.subject.name
        else:
            label = f"{i.bell}. {i.subject.nomn}"
        keyboard.add(
            Text(
                label=label,
                payload={"lesson": i.bell, "subject": i.subject.label}
            ), row=2
        )
    return keyboard


REPLACE_DAY_KEYBOARD = Keyboard(inline=False)
REPLACE_DAY_KEYBOARD.add(Text("На завтра", {"replace_day": "tomorrow"}), color=KeyboardButtonColor.POSITIVE)
REPLACE_DAY_KEYBOARD.add(Text("Свой день", {"replace_day": "custom"}), color=KeyboardButtonColor.PRIMARY)
REPLACE_DAY_KEYBOARD.row()
REPLACE_DAY_KEYBOARD.add(Text("Вернуться в меню", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
REPLACE_DAY_KEYBOARD = REPLACE_DAY_KEYBOARD.get_json()

REPLACES_TYPES_KEYBOARD = (
    Keyboard()
    .add(Text("Нет урока", {"replace_type": "no_lesson"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Другой урок", {"replace_type": "lesson_changed"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Другой учитель", {"replace_type": "teacher_changed"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Другой кабинет", {"replace_type": "room_changed"}), color=KeyboardButtonColor.PRIMARY)
) + BACK_TO_MENU
REPLACES_TYPES_KEYBOARD = REPLACES_TYPES_KEYBOARD.get_json()
