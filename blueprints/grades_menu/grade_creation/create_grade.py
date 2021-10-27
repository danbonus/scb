from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import PASS_KEYBOARD, RETURN_KEYBOARD
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Grade creation"


@bp.on.message(text=["1", "Создать"], state=GradesMenuStates.CMD_CHOICE)
async def create_grade(message: Message, scb: SCB):
    scb.storage["schedule"] = {}
    scb.storage["subjects"] = {}
    scb.storage["album_id"] = None

    await message.answer(scb.phrases.grade_creation.enter_label, keyboard=RETURN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.LABEL)


@bp.on.message(state=GradeCreationStates.LABEL)
async def grade_label(message: Message, scb: SCB):
    if not message.text:
        return scb.phrases.grade_creation.wrong_label

    scb.storage["label"] = message.text

    await message.answer(scb.phrases.grade_creation.enter_album_id, keyboard=PASS_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.ALBUM_id)
