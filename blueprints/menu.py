from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message

from constants import MENU_KEYBOARD, WRITER_KEYBOARD, ADMIN_MENU_KEYBOARD
from utils.args_object import SCB


bp = Blueprint()
bp.name = "Menu"
#  phrases.load(Menu)


@bp.on.message()
async def menu(message: Message, scb: SCB):
    if scb.user.is_admin:
        await message.answer(scb.phrases.menu.admins.safe_substitute(), keyboard=ADMIN_MENU_KEYBOARD)
    elif scb.user.is_writer:
        await message.answer(scb.phrases.menu.user.safe_substitute(), keyboard=WRITER_KEYBOARD)
    else:
        await message.answer(scb.phrases.menu.user.safe_substitute(), keyboard=MENU_KEYBOARD)
