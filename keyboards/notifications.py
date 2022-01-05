from vkbottle import KeyboardButtonColor, Text, EMPTY_KEYBOARD
from .misc import BACK_TO_MENU
from vkbottle_overrides import Keyboard

NOTIFY_TYPES_KEYBOARD = (
    Keyboard()
    .add(Text("Все пользователи", {"registered": True}))
    .add(Text("Райтеры", {"is_writer": True}))
    .row()
    .add(Text("Химия, ЕГЭ", {"exam_group": 1}))
    .add(Text("Химия, неЕГЭ", {"exam_group": 2}))
    .row()
    .add(Text("Английский, П. Д.", {"lang_group": 1}))
    .add(Text("Английский, О. Н.", {"lang_group": 2}))

) + BACK_TO_MENU
NOTIFY_TYPES_KEYBOARD = NOTIFY_TYPES_KEYBOARD.get_json()
