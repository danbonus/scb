from constants import RegistrationStates
from keyboards.grades import grades_iteration
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Registration"


@bp.on.private_message(NotRegistered=True)
async def registration_handler(message: Message, scb: SCB):
    languages, keyboard = grades_iteration(await scb.grades.list)

    await message.answer(scb.phrases.registration.reg_grade.safe_substitute(grades=languages),
                         keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)
