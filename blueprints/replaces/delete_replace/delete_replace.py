from vkbottle.bot import Message

from constants.states import ReplaceCreationStates
from keyboards.replaces import REPLACE_DAY_KEYBOARD
from rules.IsWriter import IsWriter
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Delete replace "
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(text="Удалить замену")
@bp.on.private_message(payload={"cmd": "delete_replace"})
async def add_homework(message: Message, scb: SCB):
    sent = await message.answer("beu", keyboard=REPLACE_DAY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_DAY)
