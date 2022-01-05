from vkbottle.bot import Message

from constants.states import HomeworkCreationStates
from keyboards.misc import END_KEYBOARD
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from datetime import datetime

bp = Blueprint()
bp.name = "HW ADD: deadline"


@bp.on.private_message(
    func=lambda message: len(message.text) != 0 and message.payload == {"action": "completed"},
    state=HomeworkCreationStates.OPTIONAL,
    blocking=False
)
async def deadline(message: Message, scb: SCB):
    print(message.payload)
    print(message.payload != {"action": "completed"})
    if not scb.storage["deadline"]:
        scb.storage["deadline"] = message.text
        await message.answer(message="ок, дедлайн указан.", keyboard=END_KEYBOARD)
