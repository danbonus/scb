from constants import RegistrationStates
from keyboards.grades import grades_iteration
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "First Entry"


@bp.on.private_message(FirstEntry=True)
async def first_entry_handler(message: Message, scb: SCB):
    #languages, keyboard = languages_iteration(scb.phrases.languages)
    languages, keyboard = grades_iteration(await scb.grades.list)

    await message.answer(scb.phrases.registration.reg_grade.safe_substitute(grades=languages), keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)
