import json

from vkbottle.bot import Message

from constants.states import ReplaceCreationStates
from keyboards.replaces import REPLACES_TYPES_KEYBOARD
from rules.IsWriter import IsWriter
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Replace creation: GET_LESSON"
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(state=ReplaceCreationStates.GET_LESSON)
async def add_homework(message: Message, scb: SCB):
    payload = json.loads(message.payload)
    scb.storage["replace_lesson"] = payload["lesson"]
    scb.storage["replace_subject"] = payload["subject"]
    sent = await message.answer("beu", keyboard=REPLACES_TYPES_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_TYPE)