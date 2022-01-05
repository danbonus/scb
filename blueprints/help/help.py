from vkbottle.bot import Message

from keyboards.menu import MENU_KEYBOARD, WRITER_KEYBOARD, ADMIN_MENU_KEYBOARD
from logger import logger
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Help"


@bp.on.private_message(payload={"cmd": "help"})
@bp.on.private_message(text="Помощь")
async def help(message: Message, scb: SCB):
    return 'здесь пока ничего нет'
