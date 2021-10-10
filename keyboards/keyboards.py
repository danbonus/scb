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
)
