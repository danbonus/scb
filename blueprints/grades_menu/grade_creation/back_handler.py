from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD, FIRST_BELL
from constants.states import GradesMenuStates, GradeCreationStatesList, GradeCreationStates
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Back Handler"


@bp.on.message(text="Вернуться", state=GradeCreationStatesList)
async def grade_album_id_pass(message: Message, scb: SCB):
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates(message.state_peer.state - 1))
    return "*Вы возвращены в предыдущий пункт*"