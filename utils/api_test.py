from vkbottle import Callback, KeyboardButtonColor

from vkbottle_overrides import Keyboard


class Pagination:
    def __init__(self, list_, size, payload, inline, count=None, pagination_type="adding", offset=0):
        self.list = list_
        self.size = size
        self.payload = payload
        self.inline = inline
        self.count = count
        self.type = pagination_type
        self.offset = offset

    def get(self):
        chunks = list(self.chunks(self.list, self.size, self.count))
        keyboard = Keyboard()
        if not len(chunks):
            return [], keyboard
        list_page = chunks[0]
        pages_count = len(chunks)
        NEXT_KEYBOARD = (
            Keyboard(one_time=False, inline=self.inline)
                .row()
                .add(Callback(f"1 / {pages_count}", payload={"easter": "беу)"}), color=KeyboardButtonColor.POSITIVE)
                .add(Callback("➡", payload={"page": 2, "type": self.type, 'offset': self.offset + 8}), color=KeyboardButtonColor.POSITIVE)
        )

        if self.payload:
            if 'page' in self.payload:
                if self.type == 'removing':
                    visible_page = self.payload["page"]
                    chunks_index = self.offset / 8
                    print(chunks)

                    if chunks_index == 1:
                        keyboard = NEXT_KEYBOARD

                    elif chunks_index == self.count / 8:
                        PREVIOUS_KEYBOARD = (
                            Keyboard(one_time=False, inline=self.inline)
                                .row()
                                .add(Callback("⬅", payload={"page": visible_page - 1, "type": self.type, 'offset': self.offset - 8}), color=KeyboardButtonColor.POSITIVE)
                                .add(Callback(f"{pages_count} / {pages_count}", payload={"easter": "беу)"}), color=KeyboardButtonColor.POSITIVE)
                        )

                        keyboard = PREVIOUS_KEYBOARD

                    else:
                        BOTH_KEYBOARD = (
                            Keyboard(one_time=False, inline=self.inline)
                                .row()
                                .add(Callback("⬅", payload={"page": visible_page - 1, "type": self.type, 'offset': self.offset - 8}), color=KeyboardButtonColor.POSITIVE)
                                .add(Callback(f"{visible_page} / {pages_count}", payload={"easter": "беу)"}))
                                .add(Callback("➡", payload={"page": visible_page + 1, "type": self.type, 'offset': self.offset + 8}), color=KeyboardButtonColor.POSITIVE)
                        )

                        keyboard = BOTH_KEYBOARD
                else:
                    visible_page = self.payload["page"]
                    chunks_index = visible_page - 1
                    print(chunks)
                    list_page = chunks[chunks_index]
                    print(list_page)
                    if chunks[0] == list_page:
                        keyboard = NEXT_KEYBOARD

                    elif chunks[-1] == list_page:
                        PREVIOUS_KEYBOARD = (
                            Keyboard(one_time=False, inline=self.inline)
                                .row()
                                .add(Callback("⬅", payload={"page": visible_page - 1, "type": self.type,
                                                            'offset': self.offset - 10}),
                                     color=KeyboardButtonColor.POSITIVE)
                                .add(Callback(f"{pages_count} / {pages_count}", payload={"easter": "беу)"}),
                                     color=KeyboardButtonColor.POSITIVE)
                        )

                        keyboard = PREVIOUS_KEYBOARD

                    else:
                        BOTH_KEYBOARD = (
                            Keyboard(one_time=False, inline=self.inline)
                                .row()
                                .add(Callback("⬅", payload={"page": visible_page - 1, "type": self.type,
                                                            'offset': self.offset - 10}),
                                     color=KeyboardButtonColor.POSITIVE)
                                .add(Callback(f"{visible_page} / {pages_count}", payload={"easter": "беу)"}))
                                .add(Callback("➡", payload={"page": visible_page + 1, "type": self.type,
                                                            'offset': self.offset + 10}),
                                     color=KeyboardButtonColor.POSITIVE)
                        )

                        keyboard = BOTH_KEYBOARD
            else:
                if len(chunks) > 1:
                    keyboard = NEXT_KEYBOARD

        else:  # без нажатия кнопок -> <-
            if len(chunks) > 1:
                keyboard = NEXT_KEYBOARD

        return list_page, keyboard

    def chunks(self, lst, n, length=None):
        """Yield successive n-sized chunks from lst."""
        if length:
            length = length
        else:
            length = len(lst)
        print(length)
        for i in range(0, length, n):
            yield lst[i:i + n]
