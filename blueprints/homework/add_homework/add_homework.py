from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates
from constants.keyboards import RETURN_KEYBOARD
from rules.IsWriter import IsWriter
from logger import logger
from modules.add_homework import get_subjects
bp = Blueprint()
bp.name = "HW ADD"
bp.labeler.auto_rules.append(IsWriter())


@bp.on.message(text="Добавить запись")
@bp.on.message(payload={"cmd": "add_homework"})
async def add_homework(message: Message, scb: SCB):
    keyboard = await get_subjects(scb, None)
    sent = await message.answer("beu", keyboard=keyboard + RETURN_KEYBOARD)
    scb.storage["message_ids"] = sent
    scb.storage["message_text"] = "beu"
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.GET_SUBJECT)
