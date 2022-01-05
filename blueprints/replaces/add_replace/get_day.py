from vkbottle import Text, EMPTY_KEYBOARD
from vkbottle.bot import Message

from constants.states import ReplaceCreationStates
from keyboards.misc import RETURN_KEYBOARD, BACK_TO_MENU
from rules.IsWriter import IsWriter
from utils.args_object import SCB
from vkbottle_overrides import Keyboard
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Replace creation: GET_DAY"
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(text="На завтра", state=ReplaceCreationStates.GET_DAY)
@bp.on.private_message(payload={"replace_day": "tomorrow"}, state=ReplaceCreationStates.GET_DAY)
async def add_homework(message: Message, scb: SCB):
    this_day, tomorrow_day = scb.time.get_days_of_school()
    scb.storage["replace_day"] = tomorrow_day.timestamp()
    schedule = scb.schedule[str(tomorrow_day.weekday())]
    keyboard = Keyboard(inline=False)
    for i in schedule:
        if i.subject.lang_group or i.subject.exam_group:
            label = f"{i.bell}. {i.subject.nomn}" + i.subject.name
        else:
            label = f"{i.bell}. {i.subject.nomn}"
        keyboard.add(
            Text(
                label=label,
                 payload={"lesson": i.bell, "subject": i.subject.label}
                 ), row=2
        )
    sent = await message.answer("beu", keyboard=keyboard + BACK_TO_MENU)
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_LESSON)


@bp.on.private_message(text="Свой день", state=ReplaceCreationStates.GET_DAY)
@bp.on.private_message(payload={"replace_day": "custom"}, state=ReplaceCreationStates.GET_DAY)
@bp.on.private_message(state=ReplaceCreationStates.GET_DAY)
async def add_homework(message: Message, scb: SCB):
    sent = await message.answer("введи свой день", keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_CUSTOM_DAY)
