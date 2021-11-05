from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates
from modules.homework_created import final

bp = Blueprint()
bp.name = "HW ADD: final"


@bp.on.message(text="Завершить", state=HomeworkCreationStates.OPTIONAL, blocking=False)
async def homework_end(message: Message, scb: SCB):
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.FILLED)


@bp.on.message(state=HomeworkCreationStates.FILLED)
async def homework_final(message: Message, scb: SCB):  # CALL MENU
    await bp.state_dispenser.delete(message.peer_id)
    await final(message, scb)
    message.text = "дз"
    print(bp.handlers)
    await scb.context["handlers"]["homework"].handle(message, scb)
