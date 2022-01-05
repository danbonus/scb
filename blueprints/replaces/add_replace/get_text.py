from vkbottle.bot import Message

from constants.states import ReplaceCreationStates
from keyboards.misc import BACK_TO_MENU
from rules.IsWriter import IsWriter
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from modules.update_homework import update_homework


bp = Blueprint()
bp.name = "Replace creation: GET_TEXT"
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(payload={"action": "completed"}, state=ReplaceCreationStates.GET_TEXT)
async def get_replace_text(message: Message, scb: SCB):
    sent = await message.answer("ок понял всё конец", keyboard=BACK_TO_MENU)
    await scb.replaces.create(
        scb.storage["replace_day"],
        scb.storage["replace_lesson"],
        scb.storage["replace_subject"],
        scb.storage["replace_type"],
        None
    )
    await bp.state_dispenser.delete(message.peer_id)
    await update_homework(message, scb)


@bp.on.private_message(state=ReplaceCreationStates.GET_TEXT)
async def get_replace_text(message: Message, scb: SCB):
    sent = await message.answer("ок понял всё", keyboard=BACK_TO_MENU)
    await scb.replaces.create(
        scb.storage["replace_day"],
        scb.storage["replace_lesson"],
        scb.storage["replace_subject"],
        scb.storage["replace_type"],
        message.text
    )
    await bp.state_dispenser.delete(message.peer_id)
