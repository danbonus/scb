from datetime import datetime
from vkbottle.bot import Message

from constants.states import ReplaceCreationStates
from keyboards.replaces import replaces_iteration
from logger import logger
from rules.IsWriter import IsWriter
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Replace creation: GET_CUSTOM_DAY"
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(state=ReplaceCreationStates.GET_CUSTOM_DAY)
async def add_homework(message: Message, scb: SCB):
    day = datetime.strptime(message.text, "%d.%m.%Y")
    scb.storage["replace_day"] = day.timestamp()
    this_day, tomorrow_day = scb.time.get_days_of_school(day)
    logger.debug(this_day)
    logger.debug(tomorrow_day)
    schedule = scb.schedule[str(this_day.weekday())]
    sent = await message.answer("беу", keyboard=replaces_iteration(schedule))
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_LESSON)
