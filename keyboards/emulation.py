from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard

EMULATION_DAY_KEYBOARD = Keyboard()
EMULATION_DAY_KEYBOARD.add(Text("С какого-то дня", {"emulation": "from"}), color=KeyboardButtonColor.PRIMARY)
EMULATION_DAY_KEYBOARD.add(Text("На какой-то день", {"emulation": "to"}), color=KeyboardButtonColor.PRIMARY)

CANCEL_EMULATION_KEYBOARD = Keyboard()
CANCEL_EMULATION_KEYBOARD.add(Text("⛔ Отключить эмуляцию", {"cmd": "emulation_off"}), color=KeyboardButtonColor.NEGATIVE)
