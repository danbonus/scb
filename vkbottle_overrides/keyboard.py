from typing import Optional
from vkbottle import KeyboardButtonColor, ABCAction
from vkbottle import Keyboard as RootKeyboard
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
