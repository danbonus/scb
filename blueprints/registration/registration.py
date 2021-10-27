from vkbottle_overrides.bot import Message

from constants.keyboards import iteration_keyboard
from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants import RegistrationStates

bp = Blueprint()
bp.name = "Registration"


@bp.on.message(NotRegistered=True)
async def registration_handler(message: Message, scb: SCB):
    languages, keyboard = iteration_keyboard(scb.phrases.languages)

    await message.answer(scb.phrases.registration.choose_language.safe_substitute(languages=languages),
                         keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.LANGUAGE_STATE)
