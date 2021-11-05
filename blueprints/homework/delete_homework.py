from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import BotLabeler, Message
from repositories.user import UserRepository
from constants import MENU_KEYBOARD
from utils.args_object import SCB
import datetime

bp = Blueprint()
bp.name = "Homework"
#  phrases.load(Menu)


@bp.on.message(text="Удалить")
@bp.on.message(payload={"cmd": "delete_homework"})
async def delete_record(message: Message, scb: SCB):

    #await get_homework(message, scb)
    pass


@bp.on.message(text="hw del <id>")
async def delete_record(message: Message, scb: SCB):
    #await get_homework(message, scb)
    pass
