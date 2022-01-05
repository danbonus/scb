from vkbottle import KeyboardButtonColor, Text, EMPTY_KEYBOARD

from vkbottle_overrides import Keyboard

YN_KEYBOARD = Keyboard()
YN_KEYBOARD.add(Text("Да", {"action": True}), color=KeyboardButtonColor.POSITIVE)
YN_KEYBOARD.add(Text("Нет", {"action": False}), color=KeyboardButtonColor.NEGATIVE)
YN_KEYBOARD = YN_KEYBOARD.get_json()

RETURN_KEYBOARD = Keyboard()
RETURN_KEYBOARD.add(Text("Вернуться", {"cmd": "back"}), color=KeyboardButtonColor.NEGATIVE)

END_KEYBOARD = Keyboard()
END_KEYBOARD.add(Text("Завершить", {"action": "completed"}), color=KeyboardButtonColor.POSITIVE)

PASS_KEYBOARD = Keyboard()
PASS_KEYBOARD.add(Text("Пропустить", {"cmd": "pass"}), color=KeyboardButtonColor.POSITIVE)
#PASS_KEYBOARD.add(Text("Вернуться", {"cmd": "back"}), color=KeyboardButtonColor.NEGATIVE)
PASS_KEYBOARD = PASS_KEYBOARD.get_json()

BACK_TO_MENU = (
    Keyboard()
    .add(Text("🏠 Вернуться в меню", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
)
