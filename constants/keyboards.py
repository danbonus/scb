from vkbottle import KeyboardButtonColor, Text, EMPTY_KEYBOARD, Callback
from vkbottle_overrides import Keyboard
import json


def iteration_keyboard(list_of_smth):
    smth_plain_list = ""
    smth_keyboard = Keyboard()
    #  LANGUAGES_KEYBOARD.buttons = []

    for smth in list_of_smth:
        smth_keyboard.add(Text(smth), row=3)
        smth_plain_list += f"-- {smth}\n"

    return smth_plain_list, smth_keyboard


def subjects_keyboard(subjects_list):
    smth_plain_list = ""
    keyboard = Keyboard()
    #  LANGUAGES_KEYBOARD.buttons = []

    for subject in subjects_list:
        keyboard.add(Text(subject.nomn, json.dumps(subject.label)), row=3)
        smth_plain_list += f"-- {subject.nomn}\n"

    return smth_plain_list, keyboard


REGISTER_KEYBOARD = Keyboard()
REGISTER_KEYBOARD.add(Text("Пройти регистрацию", {"reg": "start"}), color=KeyboardButtonColor.POSITIVE)
REGISTER_KEYBOARD = REGISTER_KEYBOARD.get_json()

YN_KEYBOARD = Keyboard()
YN_KEYBOARD.add(Text("Да", {"broadcast": True}), color=KeyboardButtonColor.POSITIVE)
YN_KEYBOARD.add(Text("Нет", {"broadcast": False}), color=KeyboardButtonColor.NEGATIVE)
YN_KEYBOARD = YN_KEYBOARD.get_json()

BROADCAST_TYPE_KEYBOARD = Keyboard()
BROADCAST_TYPE_KEYBOARD.add(Text("Время с конца последнего урока", {"time": "since"}), color=KeyboardButtonColor.PRIMARY)
BROADCAST_TYPE_KEYBOARD.row()
BROADCAST_TYPE_KEYBOARD.add(Text("Фиксированное время", {"time": "fixed"}), color=KeyboardButtonColor.SECONDARY)
BROADCAST_TYPE_KEYBOARD = BROADCAST_TYPE_KEYBOARD.get_json()

TIME_FIXED_KEYBOARD = Keyboard()
for i in ["15:30", "16:00", "16:30", "17:00", "17:30", "18:00"]:
    color = KeyboardButtonColor.SECONDARY
    if i == "16:00":
        color = KeyboardButtonColor.PRIMARY
    TIME_FIXED_KEYBOARD.add(Text(i), row=3, color=color)

TIME_FIXED_KEYBOARD = TIME_FIXED_KEYBOARD.get_json()

TIME_SINCE_KEYBOARD = Keyboard()

for i in ["00:30", "01:00", "01:30", "02:00", "02:30", "03:00"]:
    color = KeyboardButtonColor.SECONDARY
    if i == "01:00":
        color = KeyboardButtonColor.PRIMARY
    TIME_SINCE_KEYBOARD.add(Text(i), row=3, color=color)

TIME_SINCE_KEYBOARD = TIME_SINCE_KEYBOARD.get_json()


MENU_KEYBOARD = (
    Keyboard()
    .add(Text("Помощь"))
    .add(Text("ДЗ"))
    .add(Text("Рассылка"))
).get_json()

WRITER_KEYBOARD = (
    Keyboard()
    .add(Text("Добавить запись"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Показать ДЗ"), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("🕒 Эмуляция дня", {"cmd": "emulation"}))
).get_json()

ADMIN_MENU_KEYBOARD = (
    Keyboard()
    .add(Text("Помощь"))
    .add(Text("ДЗ"))
    .add(Text("Рассылка"))
    .row()
    .add(Text("Классы"))
).get_json()

GRADES_KEYBOARD = Keyboard()
GRADES_KEYBOARD.add(Text("Создать"), color=KeyboardButtonColor.POSITIVE)
GRADES_KEYBOARD.add(Text("Удалить"), color=KeyboardButtonColor.NEGATIVE)
GRADES_KEYBOARD.row()
GRADES_KEYBOARD.add(Text("Редактировать"), color=KeyboardButtonColor.PRIMARY)
GRADES_KEYBOARD.row()
GRADES_KEYBOARD.add(Text("Список классов"), color=KeyboardButtonColor.PRIMARY)
GRADES_KEYBOARD.row()
GRADES_KEYBOARD.add(Text("Назад", {"cmd": "back"}), color=KeyboardButtonColor.SECONDARY)
GRADES_KEYBOARD = GRADES_KEYBOARD.get_json()


PASS_KEYBOARD = Keyboard()
PASS_KEYBOARD.add(Text("Пропустить"), color=KeyboardButtonColor.POSITIVE)
PASS_KEYBOARD.add(Text("Вернуться"), color=KeyboardButtonColor.NEGATIVE)
PASS_KEYBOARD = PASS_KEYBOARD.get_json()

FIRST_BELL = Keyboard()
FIRST_BELL.add(Text("0"), color=KeyboardButtonColor.PRIMARY)
FIRST_BELL.add(Text("1"), color=KeyboardButtonColor.PRIMARY)

END_KEYBOARD = Keyboard()
END_KEYBOARD.add(Text("Завершить"), color=KeyboardButtonColor.POSITIVE)
END_KEYBOARD = END_KEYBOARD

LANGUAGES_KEYBOARD = Keyboard()

RETURN_KEYBOARD = Keyboard()
RETURN_KEYBOARD.add(Text("Вернуться"), color=KeyboardButtonColor.NEGATIVE)

CREATE_SUBJECT_KEYBOARD = Keyboard()
CREATE_SUBJECT_KEYBOARD.add(Text("Создать свой"))

SUBJECTS_KEYBOARD = Keyboard()

SUBJECTS_END_KEYBOARD = Keyboard()
SUBJECTS_END_KEYBOARD.add(Text("Все предметы указаны"))

GRADE_KEYBOARD = Keyboard()

HOMEWORK_CREATION_KEYBOARD = Keyboard()
HOMEWORK_CREATION_KEYBOARD.add(Text("Сдать до"), color=KeyboardButtonColor.PRIMARY)
HOMEWORK_CREATION_KEYBOARD.add(Text("Завершить"), color=KeyboardButtonColor.POSITIVE)

HOMEWORK_TEXT_KEYBOARD = Keyboard()
HOMEWORK_TEXT_KEYBOARD.add(Text("Ничего"), color=KeyboardButtonColor.POSITIVE)

LAST_HOMEWORK_KEYBOARD = Keyboard()
LAST_HOMEWORK_KEYBOARD.add(Text("Прошлое ДЗ", {"last_hw": True}), color=KeyboardButtonColor.PRIMARY)

EMULATION_DAY_KEYBOARD = Keyboard()
EMULATION_DAY_KEYBOARD.add(Text("С какого-то дня", {"emulation": "from"}), color=KeyboardButtonColor.PRIMARY)
EMULATION_DAY_KEYBOARD.add(Text("На какой-то день", {"emulation": "to"}), color=KeyboardButtonColor.PRIMARY)

CANCEL_EMULATION_KEYBOARD = Keyboard()
CANCEL_EMULATION_KEYBOARD.add(Text("⛔ Отключить эмуляцию"), color=KeyboardButtonColor.NEGATIVE)
CANCEL_EMULATION_KEYBOARD = CANCEL_EMULATION_KEYBOARD.get_json()

INLINE_HOMEWORK_KEYBOARD = Keyboard(one_time=False, inline=True)
INLINE_HOMEWORK_KEYBOARD.add(Callback("Предыдущий день", {''}))

HOMEWORK_OPERATIONS_KEYBOARD = Keyboard()
HOMEWORK_OPERATIONS_KEYBOARD.add(Text("Добавить", {"cmd": "add_homework"}), color=KeyboardButtonColor.POSITIVE)
HOMEWORK_OPERATIONS_KEYBOARD.add(Text("Редактировать", {"cmd": "edit_homework"}), color=KeyboardButtonColor.POSITIVE)
HOMEWORK_OPERATIONS_KEYBOARD.row()
HOMEWORK_OPERATIONS_KEYBOARD.add(Text("Удалить", {"cmd": "delete_homework"}), color=KeyboardButtonColor.PRIMARY)
HOMEWORK_OPERATIONS_KEYBOARD.row()
HOMEWORK_OPERATIONS_KEYBOARD.add(Text("Эмуляция дня", {"cmd": "emulation"}), color=KeyboardButtonColor.SECONDARY)
HOMEWORK_OPERATIONS_KEYBOARD.row()
HOMEWORK_OPERATIONS_KEYBOARD.add(Text("Вернуться", {"cmd": "back"}), color=KeyboardButtonColor.NEGATIVE)
HOMEWORK_OPERATIONS_KEYBOARD = HOMEWORK_OPERATIONS_KEYBOARD.get_json()
