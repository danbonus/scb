from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard

MENU_KEYBOARD = (
    Keyboard()
    .add(Text("ℹ️ Помощь", {"cmd": "help"}))
    .add(Text("📚 ДЗ", {"cmd": "show_homework"}))
    .add(Text("💌 Рассылка", {"cmd": "broadcast"}))
).get_json()

WRITER_KEYBOARD = (
    Keyboard()
    .add(Text("📝 Добавить запись", {"cmd": "add_homework"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("🔄 Добавить замену", {"cmd": "add_replace"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("📚 Показать ДЗ", {"cmd": "show_homework"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("🔔 Оповестить", {"cmd": "notify"}))
    .add(Text("🕒 Эмуляция дня", {"cmd": "emulation"}))
).get_json()

ADMIN_MENU_KEYBOARD = (
    Keyboard()
    .add(Text("Помощь", {"cmd": "help"}))
    .add(Text("📚 ДЗ", {"cmd": "show_homework"}))
    .add(Text("💌 Рассылка", {"cmd": "broadcast"}))
    .row()
    .add(Text("Классы"))
).get_json()
