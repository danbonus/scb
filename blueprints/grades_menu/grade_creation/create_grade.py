from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Grade creation"


@bp.on.message(text=["1", "Создать"], state=GradesMenuStates.CMD_CHOICE)
async def create_grade(message: Message, scb: SCB):
    await message.answer(scb.phrases.grades.enter_label)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.LABEL)


@bp.on.message(state=GradeCreationStates.LABEL)
async def grade_label(message: Message, scb: SCB):
    if not message.text:
        return scb.phrases.grades.wrong_label

    scb.storage.set(message.peer_id, {
        "label": message.text,
        "album_id": None,
        "lang": None,
        "subject_label": None,
        "first_bell": None,
        "bells": {},
        "subjects": {},
        "schedule": {}
    })
    await message.answer(scb.phrases.grades.enter_album_id, keyboard=PASS_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.ALBUM_id)


