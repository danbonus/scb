from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message

from constants import MENU_KEYBOARD, ADMIN_MENU_KEYBOARD
from utils.args_object import SCB


bp = Blueprint()
bp.name = "Menu"
#  phrases.load(Menu)



@bp.on.message(IsAdmin=True)
async def admin_menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.admins_menu, keyboard=ADMIN_MENU_KEYBOARD)

@bp.on.message(IsWriter=True)
async def writer_menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu, keyboard=MENU_KEYBOARD)

@bp.on.message()
async def menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu,keyboard=MENU_KEYBOARD)
