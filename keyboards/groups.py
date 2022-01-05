from vkbottle import KeyboardButtonColor, Text

from vkbottle_overrides import Keyboard


def groups_iteration(groups_list):
    groups_plain = ""
    groups_keyboard = Keyboard()

    for group in groups_list:
        groups_keyboard.add(Text(group.name, {"group": group.num}), row=1, color=KeyboardButtonColor.PRIMARY)
        groups_plain += f"-- {group}\n"

    return groups_plain, groups_keyboard
