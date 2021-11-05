from vkbottle import Text, KeyboardButtonColor, Callback
from vkbottle_types import GroupTypes

from logger import logger
from models.subject import SingleSubject
from vkbottle_overrides import Keyboard
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates
from constants.keyboards import HOMEWORK_TEXT_KEYBOARD, LAST_HOMEWORK_KEYBOARD
import json

bp = Blueprint()
bp.name = "Hw add: subject"


@bp.on.message_event(payload_map={"name": str})
async def set_group(event: GroupTypes.MessageEvent, scb: SCB):
    msg_id = scb.storage["message_ids"]
    subject = scb.subjects[scb.storage["subject_to_fill"]]
    payload = event.object.payload["name"]
    keyboard = Keyboard(inline=True)

    groups = await scb.subjects.find_groups(subject.label)
    if payload == "both":
        scb.storage["subject_to_fill"] = [i.label for i in groups]
        for i in groups:
            color = KeyboardButtonColor.PRIMARY

            keyboard.add(Callback(i.name, {"name": i.label}), color=color)
        keyboard.row()
        keyboard.add(Callback("Обе группы", {"name": "both"}), color=KeyboardButtonColor.POSITIVE)
    else:
        group = scb.subjects[payload]

        for i in groups:
            if group.label == i.label:
                scb.storage["subject_to_fill"] = i.label
                color = KeyboardButtonColor.POSITIVE
            else:
                color = KeyboardButtonColor.PRIMARY

            keyboard.add(Callback(i.name, {"name": i.label}), color=color)

        keyboard.row()
        keyboard.add(Callback("Обе группы", {"name": "both"}), color=KeyboardButtonColor.SECONDARY)

    await bp.api.messages.edit(
        peer_id=event.object.user_id,
        user_id=event.object.user_id,
        message_id=msg_id,
        message="выбери",
        keyboard=keyboard.get_json()
    )


@bp.on.message(state=HomeworkCreationStates.GET_SUBJECT)
async def get_subject(message: Message, scb: SCB):
    if message.payload:
        scb.storage["subject_to_fill"] = (subject := json.loads(message.payload))
        subject = scb.subjects[subject]
    else:
        subject: SingleSubject = await scb.subjects.is_subject(message)
        if not subject:
            return "неизвестный предмет"

    keyboard = HOMEWORK_TEXT_KEYBOARD
    if await scb.homework.get_last_homework(subject.label):
        keyboard = keyboard + LAST_HOMEWORK_KEYBOARD

    await message.answer(
        message="окей, предмет %s. введи текст или на кнопки нажми." % subject.nomn,
        keyboard=keyboard
    )

    groups = await scb.subjects.find_groups(subject.label)
    logger.debug(groups)
    if groups:
        logger.debug("Lang group detected")
        keyboard = Keyboard(inline=True)
        for i in await scb.subjects.find_groups(subject.label):
            if i.lang_group == scb.user.lang_group or i.ege_group == scb.user.ege_group:
                color = KeyboardButtonColor.POSITIVE
            else:
                color = KeyboardButtonColor.PRIMARY
            keyboard.add(Callback(i.name, {"name": i.label}), color=color)
        sent = await message.answer(message="ок, выбери группу", keyboard=keyboard.get_json())
        scb.storage["message_ids"] = sent

    if subject.ege_group:
        return "егэ не егэ"

    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.HOMEWORK_TEXT)
