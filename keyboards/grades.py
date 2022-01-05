from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard


def grades_iteration(grades_list):
    grades_plain = ""
    grades_keyboard = Keyboard()
    #  LANGUAGES_KEYBOARD.buttons = []

    for grade in grades_list:
        grades_keyboard.add(Text(grade.label, {"grade": grade.id}), row=3)
        grades_plain += f"-- {grade}\n"

    return grades_plain, grades_keyboard


FIRST_BELL = (
    Keyboard()
    .add(Text("0"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("1"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Вернуться в меню", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
)

GRADES_KEYBOARD = (
    Keyboard()
    .add(Text("Создать", {"cmd": "create_grade"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Удалить", {"cmd": "delete_grade"}), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Редактировать", {"cmd": "edit_grade"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Список классов", {"cmd": "show_grades"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Вернуться в меню", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
).get_json()
