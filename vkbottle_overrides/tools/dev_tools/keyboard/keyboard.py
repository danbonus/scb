from typing import Optional
from vkbottle import Keyboard as RootKeyboard
from vkbottle import KeyboardButtonColor, ABCAction
from vkbottle.tools.dev_tools.keyboard.button import KeyboardButton


class Keyboard(RootKeyboard):
    def add(self, action: ABCAction, row: int = 5, color: Optional[KeyboardButtonColor] = None) -> "Keyboard":
        if not len(self.buttons):
            self.row()
        if len(self.buttons[-1]) == row:
            self.row()
        button = KeyboardButton.from_typed(action, color)
        self.buttons[-1].append(button)
        return self

    def __add__(self, other_keyboard: RootKeyboard):
        temp_keyboard = Keyboard(one_time=self.one_time, inline=self.inline)
        temp_keyboard.buttons.extend(self.buttons)
        temp_keyboard.buttons.extend(other_keyboard.buttons)
        return temp_keyboard
