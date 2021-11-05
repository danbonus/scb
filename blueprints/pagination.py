from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates
from constants.keyboards import RETURN_KEYBOARD
import json
from vkbottle import GroupEventType, GroupTypes
from rules.IsWriter import IsWriter
from logger import logger
from modules.add_homework import get_subjects
from .homework.homework import get_homework
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
import datetime
from string import Template
from random import randint
from rules.IsWriter import IsWriter
import json
from vkbottle import GroupEventType, GroupTypes
from vkbottle import KeyboardButtonColor, Text, EMPTY_KEYBOARD, Callback
from vkbottle_overrides import Keyboard
from constants.keyboards import RETURN_KEYBOARD
from datetime import timedelta


bp = Blueprint()
bp.name = "Pagination"


@bp.on.message_event(payload_map={"page": int})
async def subject_pagination(event: GroupTypes.MessageEvent, scb):
    keyboard = await get_subjects(scb, event.object.payload)
    await bp.api.messages.edit(
        peer_id=event.object.peer_id,
        user_id=event.object.user_id,
        message_id=scb.storage["message_ids"],
        message=scb.storage["message_text"],
        keyboard=keyboard + RETURN_KEYBOARD
    )


@bp.on.message_event(payload_map={"date": str})
async def date_pagination(event: GroupTypes.MessageEvent, scb):
    date_plain = event.object.payload["date"]
    date = datetime.datetime.strptime(date_plain, "%d.%m.%y")
    date_back = (date - timedelta(days=1))
    date_up = (date + timedelta(days=1))
    if date_back.weekday() == 6:
        date_back = date_back - timedelta(days=1)
    if date_up.weekday() == 6:
        date_up = date_up + timedelta(days=1)

    date_back_word = scb.phrases.constants.days[str(date_back.weekday())]
    date_up_word = scb.phrases.constants.days[str(date_up.weekday())]

    keyboard = Keyboard(inline=True)
    keyboard.add(Callback(f"◀️", {"date": date_back.strftime("%d.%m.%y")}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Callback(date_plain, {"date": date_plain}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Callback(f"▶️", {"date": date_up.strftime("%d.%m.%y")}), color=KeyboardButtonColor.SECONDARY)
    await get_homework(None, scb, date=date, send=False)
    #if scb.storage("message_ids") > 1:
        #await get_homework(None, scb, date=date, send=False)
        # if scb.storage("message_texts") > 1:

    for num, i in enumerate(scb.storage["message_ids"]):
        logger.debug("updating")
        await bp.api.messages.edit(
            peer_id=event.object.user_id,
            user_id=event.object.user_id,
            message_id=i,
            message=scb.storage["message_text"][num],
            keyboard=keyboard.get_json()
        )


@bp.on.message_event(payload_map={"page": str, "grade": str})
async def grades_pagination(event: GroupTypes.MessageEvent, scb):
    pass
