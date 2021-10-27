from typing import Set, Tuple, Union
import re
from logger import logger
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union
from vkbottle.bot import BotLabeler
from vkbottle_overrides.dispatch.rules.abc import ABCRule
from vkbottle_overrides.tools.dev_tools.utils import convert_shorten_filter
from vkbottle_overrides.dispatch.views.bot import MessageView, RawEventView
from vkbottle_overrides.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle.framework.bot.labeler.abc import LabeledMessageHandler
import vbml
from constants.keyboards import Keyboard, Text, KeyboardButtonColor, Callback


class Pagination:
    def __init__(self, list_, size, payload):
        self.list = list_
        self.size = size
        self.payload = payload

    def get(self):
        chunks = list(self.chunks(self.list, self.size))
        keyboard = Keyboard()
        if not len(chunks):
            return [], keyboard
        list_page = chunks[0]
        pages_count = len(chunks)
        NEXT_KEYBOARD = (
            Keyboard(one_time=False, inline=False)
                .row()
                .add(Callback(f"1 / {pages_count}", payload={"easter": "беу)"}))
                .add(Callback("➡", payload={"page": 2}))
        )

        if self.payload:
            if 'page' in self.payload:
                visible_page = self.payload["page"]
                chunks_index = visible_page - 1

                list_page = chunks[chunks_index]

                if chunks[0] == list_page:
                    keyboard = NEXT_KEYBOARD

                elif chunks[-1] == list_page:
                    PREVIOUS_KEYBOARD = (
                        Keyboard(one_time=False, inline=False)
                            .row()
                            .add(Callback("⬅", payload={"page": visible_page - 1}))
                            .add(Callback(f"{pages_count} / {pages_count}", payload={"easter": "беу)"}))
                    )

                    keyboard = PREVIOUS_KEYBOARD

                else:
                    BOTH_KEYBOARD = (
                        Keyboard(one_time=False, inline=False)
                            .row()
                            .add(Callback("⬅", payload={"page": visible_page - 1}))
                            .add(Callback(f"{visible_page} / {pages_count}", payload={"easter": "беу)"}))
                            .add(Callback("➡", payload={"page": visible_page + 1}))
                    )

                    keyboard = BOTH_KEYBOARD

        else:  # без нажатия кнопок -> <-
            if len(chunks) > 1:
                keyboard = NEXT_KEYBOARD

        return list_page, keyboard

    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
