from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message
from utils.args_object import SCB
from constants.keyboards import FIRST_BELL, RETURN_KEYBOARD
from constants.states import GradeCreationStates

bp = Blueprint()
bp.name = "Album id"


@bp.on.message(text="пропустить", state=GradeCreationStates.ALBUM_id)
async def grade_album_id_pass(message: Message, scb: SCB):
    scb.storage["album_id"] = None
    await message.answer(scb.phrases.grade_creation.first_bell, keyboard=FIRST_BELL + RETURN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.FIRST_BELL)


@bp.on.message(state=GradeCreationStates.ALBUM_id)
async def grade_album_id(message: Message, scb: SCB):
    if not message.text.isdigit():
        return scb.phrases.grade_creation.wrong_album_id

    result = await scb.api.has_album(message.text)
    if not result:
        return scb.phrases.grade_creation.album_not_found

    scb.storage["album_id"] = message.text

    await message.answer(scb.phrases.grade_creation.album_title % result.title + scb.phrases.grade_creation.first_bell, keyboard=FIRST_BELL + RETURN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.FIRST_BELL)
