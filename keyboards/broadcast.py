from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard

DISABLE_BROADCAST = (
    Keyboard()
    .add(Text("Отключить рассылку", {"cmd": "disable_broadcast"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Вернуться в меню", {"cmd": "menu"}))
).get_json()


BROADCAST_TIME_KEYBOARD = (
    Keyboard()
    .add(Text("Через полчаса", {"broadcast_time": "00:30"}))
    .row()
    .add(Text("Через час", {"broadcast_time": "01:00"}))
    .row()
    .add(Text("Через 1.5 часа", {"broadcast_time": "01:30"}))
).get_json()

