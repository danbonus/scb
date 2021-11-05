from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates

bp = Blueprint()
bp.name = "HW ADD: deadline"


@bp.on.message(
    func=lambda message: len(message.text) != 0 and message.text != "Завершить",
    state=HomeworkCreationStates.OPTIONAL,
    blocking=False
)
async def deadline(message: Message, scb: SCB):
    if not scb.storage["deadline"]:
        scb.storage["deadline"] = message.text
        return "ок, дедлайн указан."
