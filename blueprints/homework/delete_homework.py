from vkbottle.bot import Message

from keyboards.misc import YN_KEYBOARD, BACK_TO_MENU
from modules.get_subjects_to_delete import get_subjects_to_delete
from modules.update_homework import update_homework
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
import json

from vkbottle import KeyboardButtonColor, Callback
from vkbottle.bot import Message
from vkbottle_types import GroupTypes

from constants.states import HomeworkCreationStates, HomeworkDeletionStates
from keyboards.homework import NO_HOMEWORK_GIVEN, LAST_HOMEWORK_KEYBOARD
from logger import logger
from models.subject import SingleSubject
from utils.args_object import SCB
from vkbottle_overrides import Keyboard
from vkbottle_overrides.bot import Blueprint
bp = Blueprint()
bp.name = "Homework: Delete"
#  phrases.load(Menu)


@bp.on.private_message(text="Удалить")
@bp.on.private_message(payload={"cmd": "delete_homework"})
async def delete_record(message: Message, scb: SCB):
    scb.storage["skip_filled"] = False
    scb.storage["skip_foreign_groups"] = False
    keyboard = await get_subjects_to_delete(scb, {})
    sent = await message.answer("beu", keyboard=keyboard + BACK_TO_MENU)
    scb.storage["message_ids"] = sent
    scb.storage["message_text"] = "beu"
    await bp.state_dispenser.set(message.peer_id, HomeworkDeletionStates.GET_SUBJECT)

    #await get_homework(message, scb)
    pass


@bp.on.private_message(payload_map={"homework_id": int}, state=HomeworkDeletionStates.GET_SUBJECT)
async def delete_record(message: Message, scb: SCB):
    payload = json.loads(message.payload)
    record = await scb.homework.get_by_id(payload["homework_id"])
    scb.storage["homework_id"] = payload["homework_id"]
    subject = scb.subjects[record.subject]
    await message.answer(f"Нашел! \nПредмет: {subject.nomn}\nДомашка: {record.homework}\n\nУдаляю?", keyboard=YN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, HomeworkDeletionStates.CONFIRM)


@bp.on.private_message(payload={"action": True}, state=HomeworkDeletionStates.CONFIRM)
async def confirm(message: Message, scb: SCB):
    result = await scb.homework.delete(scb.storage["homework_id"])
    await message.answer(result, keyboard=BACK_TO_MENU)
    await bp.state_dispenser.delete(message.peer_id)
    await update_homework(message, scb)


@bp.on.private_message(text="hw del <id>")
async def delete_record(message: Message, scb: SCB):
    #await get_homework(message, scb)
    pass
