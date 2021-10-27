from vkbottle_overrides.bot import Message

from constants.keyboards import iteration_keyboard
from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants import RegistrationStates

bp = Blueprint()
bp.name = "First Entry"


@bp.on.message(FirstEntry=True)
async def first_entry_handler(message: Message, scb: SCB):
    languages, keyboard = iteration_keyboard(scb.phrases.languages)
    await message.answer(scb.phrases.registration.first_entry.safe_substitute(languages=languages), keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.LANGUAGE_STATE)
