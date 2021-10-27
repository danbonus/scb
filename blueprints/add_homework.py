from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import BotLabeler, Message
from repositories.user import UserRepository
from constants import MENU_KEYBOARD
from utils.args_object import SCB


bp = Blueprint()
bp.name = "HW ADD"
#  phrases.load(Menu)


@bp.on.message(text="Добавить ДЗ")
async def homework(message: Message, scb: SCB):
    user = scb.user
    grade_subjects = scb.subjects.grades_subjects
    await scb.homework.create(subject="english", homework="nothing yet", attachments=[], sender=442771271)
    return "добавлено"
