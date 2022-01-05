from vkbottle.bot import Message

from constants.states import HomeworkCreationStates
from modules.homework_created import final
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "HW ADD: optional"


@bp.on.private_message(state=HomeworkCreationStates.OPTIONAL)
async def optional(message: Message, scb: SCB):
    if scb.storage["deadline"] and scb.storage["attachments"]:
        await bp.state_dispenser.delete(message.peer_id)
        await final(message, scb)
