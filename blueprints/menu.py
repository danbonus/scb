from vkbottle.bot import Message

from keyboards.menu import MENU_KEYBOARD, WRITER_KEYBOARD, ADMIN_MENU_KEYBOARD
from logger import logger
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Menu"
#  phrases.load(Menu)


@bp.on.private_message()
async def menu(message: Message, scb: SCB):
    #logger.debug(message.payload)
    if scb.user.is_admin:
        await message.answer(scb.phrases.menu.admins.safe_substitute(), keyboard=ADMIN_MENU_KEYBOARD)
    elif scb.user.is_writer:
        await message.answer(scb.phrases.menu.user.safe_substitute(), keyboard=WRITER_KEYBOARD)
    else:
        await message.answer(scb.phrases.menu.user.safe_substitute(), keyboard=MENU_KEYBOARD)
    if message.state_peer:
        await bp.state_dispenser.delete(message.peer_id)
