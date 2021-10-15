from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD, FIRST_BELL
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Album id"


@bp.on.message(text="пропустить", state=GradeCreationStates.ALBUM_id)
async def grade_album_id_pass(message: Message, scb: SCB):
    info = scb.storage.get(message.peer_id)

    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.first_bell, keyboard=FIRST_BELL)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.FIRST_BELL)
    #await scb.grades.create(label=message.state_peer.payload["label"])

@bp.on.message(state=GradeCreationStates.ALBUM_id)
async def grade_album_id(message: Message, scb: SCB):
    if not message.text.isdigit():
        return scb.phrases.grades.wrong_album_id

    result = await scb.api.has_album(message.text)
    if not result:
        return scb.phrases.grades.album_not_found

    info = scb.storage.get(message.peer_id)
    info["album_id"] = message.text

    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.album_title % result.title + scb.phrases.grades.first_bell, keyboard=FIRST_BELL)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.FIRST_BELL)
    #await scb.grades.create(label=message.state_peer.payload["label"], album_id=message.text)
