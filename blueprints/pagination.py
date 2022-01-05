from logger import logger
from vkbottle import GroupTypes
from vkbottle import KeyboardButtonColor, Callback

from keyboards.misc import RETURN_KEYBOARD, BACK_TO_MENU
from logger import logger
from modules.add_homework import get_subjects
from modules.get_subjects_to_delete import get_subjects_to_delete
from vkbottle_overrides import Keyboard
from vkbottle_overrides.bot import Blueprint
from .homework.homework import get_homework
import datetime
from datetime import timedelta
import json


bp = Blueprint()
bp.name = "Pagination"


@bp.on.message_event(payload_map={"easter": str})
async def subject_pagination(event: GroupTypes.MessageEvent, scb):
    print('easter!')
    await event.unprepared_ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=json.dumps(
            {
                "type": "show_snackbar",
                "text": event.object.payload["easter"]
            }
        )
    )


@bp.on.message_event(payload_map={"page": int, "type": str, "offset": int})
async def subject_pagination(event: GroupTypes.MessageEvent, scb):
    skip_filled = scb.storage["skip_filled"]
    skip_foreign_groups = scb.storage["skip_foreign_groups"]
    if event.object.payload["type"] == "adding":
        keyboard = await get_subjects(scb, event.object.payload, skip_filled=skip_filled, skip_foreign_groups=skip_foreign_groups)
    else:
        keyboard = await get_subjects_to_delete(scb, event.object.payload)

    await bp.api.messages.edit(
        peer_id=event.object.peer_id,
        user_id=event.object.user_id,
        message_id=scb.storage["message_ids"],
        message=scb.storage["message_text"],
        keyboard=keyboard + BACK_TO_MENU
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
    keyboard.add(Callback(date_back.strftime("%d.%m.%y"), {"date": date_back.strftime("%d.%m.%y")}), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Callback(date_plain, {"date": date_plain}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Callback(date_up.strftime("%d.%m.%y"), {"date": date_up.strftime("%d.%m.%y")}), color=KeyboardButtonColor.PRIMARY)
    await get_homework(scb, date=date, send=False)
    #if scb.storage("message_ids") > 1:
        #await get_homework(None, scb, date=date, send=False)
        # if scb.storage("message_texts") > 1:
    logger.debug("ATtachments in pagination: %s" % scb.storage["message_attachments"])
    for num, i in enumerate(scb.storage["message_ids"]):
        logger.debug("updating")
        await bp.api.messages.edit(
            peer_id=event.object.user_id,
            user_id=event.object.user_id,
            message_id=i,
            message=scb.storage["message_text"][num],
            attachment=scb.storage["message_attachments"],
            keyboard=keyboard.get_json()
        )


@bp.on.message_event(payload_map={"page": str, "grade": str})
async def grades_pagination(event: GroupTypes.MessageEvent, scb):
    pass
