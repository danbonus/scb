from vkbottle.bot import Message

from blueprints.homework.homework import get_homework
from constants.states import HomeworkCreationStates
from modules.homework_created import final
from modules.update_homework import update_homework
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "HW ADD: final"


@bp.on.private_message(payload={"action": "completed"}, state=HomeworkCreationStates.OPTIONAL, blocking=False)
@bp.on.private_message(text="Завершить", state=HomeworkCreationStates.OPTIONAL, blocking=False)
async def homework_end(message: Message, scb: SCB):
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.FILLED)


@bp.on.private_message(state=HomeworkCreationStates.FILLED)
async def homework_final(message: Message, scb: SCB):  # CALL MENU
    await bp.state_dispenser.delete(message.peer_id)
    await final(message, scb)
    await get_homework(scb)
    await update_homework(message, scb)