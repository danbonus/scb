from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard

SDAMGIA_KEYBOARD = (
    Keyboard()
    .add(Text("Задача"))
    .add(Text("Поиск задачи по тексту"))
    .add(Text("Тест"))
    .add(Text("Поиск по изображению"))
).get_json()
