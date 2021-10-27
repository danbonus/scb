from vkbottle_overrides.bot import Message

from constants.keyboards import iteration_keyboard, EMPTY_KEYBOARD
from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants import RegistrationStates, GradeCreationStates

bp = Blueprint()
bp.name = "Registration: choose language"


@bp.on.message(state=RegistrationStates.LANGUAGE_STATE)
async def language_handler(message: Message, scb: SCB):
    if not message.text.lower() in scb.phrases.languages:
        return scb.phrases.grade_creation.wrong_language
    answer = scb.phrases.registration.reg_grade

    if not await scb.grades.list:
        await message.answer(scb.phrases.grade_creation.no_grades, keyboard=EMPTY_KEYBOARD)
        await bp.state_dispenser.set(message.peer_id, GradeCreationStates.LABEL)
        return

    grades, keyboard = iteration_keyboard([grade.label for grade in await scb.grades.list])

    await message.answer(answer.safe_substitute(grades=grades), keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)
