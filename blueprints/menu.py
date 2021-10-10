from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import BotLabeler, Message
from repositories.user import UserRepository
from keyboards import MENU_KEYBOARD
from utils import SCB


bl = BotLabeler()
bp = Blueprint()
bp.name = "Menu"
#  phrases.load(Menu)


@bp.on.message()
async def menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu,keyboard=MENU_KEYBOARD)


@bp.on.message(IsWriter=True)
async def writer_menu(message: Message, scb: SCB):
    await message.answer("neu", keyboard = MENU_KEYBOARD)
