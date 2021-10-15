from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import BotLabeler, Message
from repositories.user import UserRepository
from constants import MENU_KEYBOARD
from utils.args_object import SCB


bp = Blueprint()
bp.name = "Users Control"
#  phrases.load(Menu)


'''@bp.on.message()
async def menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu,keyboard=MENU_KEYBOARD)


@bp.on.message(IsWriter=True)
async def writer_menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu, keyboard=MENU_KEYBOARD)'''
