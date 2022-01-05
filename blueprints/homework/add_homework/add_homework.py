from vkbottle.bot import Message

from constants.states import HomeworkCreationStates
from keyboards.misc import RETURN_KEYBOARD, BACK_TO_MENU
from modules.add_homework import get_subjects
from rules.IsWriter import IsWriter
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "HW ADD"
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(text="Добавить запись")
@bp.on.private_message(payload={"cmd": "add_homework"})
async def add_homework(message: Message, scb: SCB):
    keyboard = await get_subjects(scb, None)
    scb.storage["skip_filled"] = True
    scb.storage["skip_foreign_groups"] = True
    sent = await message.answer("📗 | Выбери предмет", keyboard=keyboard + BACK_TO_MENU)
    scb.storage["message_ids"] = sent
    scb.storage["message_text"] = "📗 | Выбери предмет"
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.GET_SUBJECT)
