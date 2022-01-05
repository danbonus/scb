from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard

HOMEWORK_KEYBOARD = (
    Keyboard()
    .add(Text("📝 Добавить", {"cmd": "add_homework"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("✍️ Редактировать", {"cmd": "edit_homework"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("🗑️ Удалить", {"cmd": "delete_homework"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("📚 Показать дз еще раз :)", {"cmd": "show_homework"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("🆔 Показать id", {"cmd": "show_ids"}))
    .add(Text("👬 Показать группы", {"cmd": "show_groups"}))
    .row()
    .add(Text("🔔 Показать звонки", {"cmd": "show_bells"}))
    .add(Text("🕒 Эмуляция дня", {"cmd": "emulation"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("🏠 Вернуться в меню", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
).get_json()

USER_HOMEWORK_KEYBOARD = (
    Keyboard()
    .add(Text("📚 Показать дз еще раз :)", {"cmd": "show_homework"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("🆔 Показать id", {"cmd": "show_ids"}))
    .row()
    .add(Text("👬 Показать группы", {"cmd": "show_groups"}))
    .row()
    .add(Text("🔔 Показать звонки", {"cmd": "show_bells"}))
    .row()
    .add(Text("🏠 Вернуться в меню", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
).get_json()

NO_HOMEWORK_GIVEN = Keyboard()
NO_HOMEWORK_GIVEN.add(Text("😃 Ничего", {"no_homework_given": True}), color=KeyboardButtonColor.POSITIVE)

LAST_HOMEWORK_KEYBOARD = Keyboard()
LAST_HOMEWORK_KEYBOARD.add(Text("🗒️ Прошлое ДЗ", {"last_homework_given": True}), color=KeyboardButtonColor.PRIMARY)

DEADLINE_OR_FINISH = Keyboard()
DEADLINE_OR_FINISH.add(Text("📅 Сдать до", {"cmd": "deadline"}), color=KeyboardButtonColor.PRIMARY)
DEADLINE_OR_FINISH.add(Text("🪄 Завершить", {"action": "completed"}), color=KeyboardButtonColor.POSITIVE)
