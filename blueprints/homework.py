from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import BotLabeler, Message
from repositories.user import UserRepository
from constants import MENU_KEYBOARD
from utils.args_object import SCB


bl = BotLabeler()
bp = Blueprint()
bp.name = "Homework"
#  phrases.load(Menu)


@bp.on.message(text="ДЗ")
async def homework(message: Message, scb: SCB):


        pass