from vkbottle import KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle_overrides import Keyboard

REGISTER_KEYBOARD = Keyboard(one_time=False, inline=False)
REGISTER_KEYBOARD.add(Text("Пройти регистрацию", {"reg": "start"}), color=KeyboardButtonColor.POSITIVE)
REGISTER_KEYBOARD = REGISTER_KEYBOARD.get_json()

YN_KEYBOARD = Keyboard(one_time=False, inline=False)
YN_KEYBOARD.add(Text("Да", {"broadcast": True}), color=KeyboardButtonColor.POSITIVE)
YN_KEYBOARD.add(Text("Нет", {"broadcast": False}), color=KeyboardButtonColor.NEGATIVE)
YN_KEYBOARD = YN_KEYBOARD.get_json()

BROADCAST_TYPE_KEYBOARD = Keyboard(one_time=False, inline=False)
BROADCAST_TYPE_KEYBOARD.add(Text("Время с конца последнего урока"), color=KeyboardButtonColor.PRIMARY)
BROADCAST_TYPE_KEYBOARD.row()
BROADCAST_TYPE_KEYBOARD.add(Text("Фиксированное время"), color=KeyboardButtonColor.SECONDARY)
BROADCAST_TYPE_KEYBOARD = BROADCAST_TYPE_KEYBOARD.get_json()

TIME_FIXED_KEYBOARD = Keyboard(one_time=False, inline=False)
for i in ["15:30", "16:00", "16:30", "17:00", "17:30", "18:00"]:
    color = KeyboardButtonColor.SECONDARY
    if i == "16:00":
        color = KeyboardButtonColor.PRIMARY
    TIME_FIXED_KEYBOARD.add(Text(i), row=3, color=color)

TIME_FIXED_KEYBOARD = TIME_FIXED_KEYBOARD.get_json()

TIME_SINCE_KEYBOARD = Keyboard(one_time=False, inline=False)

for i in ["00:30", "01:00", "01:30", "02:00", "02:30", "03:00"]:
    color = KeyboardButtonColor.SECONDARY
    if i == "01:00":
        color = KeyboardButtonColor.PRIMARY
    TIME_SINCE_KEYBOARD.add(Text(i), row=3, color=color)

TIME_SINCE_KEYBOARD = TIME_SINCE_KEYBOARD.get_json()


MENU_KEYBOARD = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Помощь"))
    .add(Text("ДЗ"))
    .add(Text("Рассылка"))
).get_json()

ADMIN_MENU_KEYBOARD = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Помощь"))
    .add(Text("ДЗ"))
    .add(Text("Рассылка"))
    .row()
    .add(Text("Классы"))
).get_json()

GRADES_KEYBOARD  = Keyboard(one_time=True, inline=False)
GRADES_KEYBOARD.add(Text("Создать"), color=KeyboardButtonColor.POSITIVE)
GRADES_KEYBOARD.add(Text("Удалить"), color=KeyboardButtonColor.NEGATIVE)
GRADES_KEYBOARD.row()
GRADES_KEYBOARD.add(Text("Редактировать"), color=KeyboardButtonColor.PRIMARY)
GRADES_KEYBOARD.row()
GRADES_KEYBOARD.add(Text("Список классов"), color=KeyboardButtonColor.PRIMARY)
GRADES_KEYBOARD.row()
GRADES_KEYBOARD.add(Text("Назад", {"cmd": "back"}), color=KeyboardButtonColor.SECONDARY)
GRADES_KEYBOARD = GRADES_KEYBOARD.get_json()


PASS_KEYBOARD = Keyboard(one_time=False, inline=False)
PASS_KEYBOARD.add(Text("Пропустить"), color=KeyboardButtonColor.POSITIVE)
PASS_KEYBOARD = PASS_KEYBOARD.get_json()

FIRST_BELL = Keyboard(one_time=False, inline=False)
FIRST_BELL.add(Text("0"), color=KeyboardButtonColor.PRIMARY)
FIRST_BELL.add(Text("1"), color=KeyboardButtonColor.PRIMARY)
FIRST_BELL = FIRST_BELL.get_json()

BELLS_END = Keyboard(one_time=False, inline=False)
BELLS_END.add(Text("Конец"), color=KeyboardButtonColor.POSITIVE)
BELLS_END = BELLS_END.get_json()

LANGUAGES_KEYBOARD = Keyboard(one_time=False, inline=False)
