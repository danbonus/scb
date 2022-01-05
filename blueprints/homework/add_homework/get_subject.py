import json

from vkbottle import KeyboardButtonColor, Callback
from vkbottle.bot import Message
from vkbottle_types import GroupTypes

from constants.states import HomeworkCreationStates
from keyboards.homework import NO_HOMEWORK_GIVEN, LAST_HOMEWORK_KEYBOARD
from keyboards.misc import BACK_TO_MENU
from logger import logger
from models.subject import SingleSubject
from utils.args_object import SCB
from vkbottle_overrides import Keyboard
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Hw add: subject"


@bp.on.message_event(payload={"name": "both"})
async def both_groups(event: GroupTypes.MessageEvent, scb: SCB):
    msg_id = scb.storage["message_ids"]
    subject = scb.subjects[scb.storage["subject_to_fill"]]
    keyboard = Keyboard(inline=True)

    groups = await scb.subjects.find_groups(subject.label)
    scb.storage["subject_to_fill"] = [i.label for i in groups]
    scb.storage["readable_subject_name"] = [i.nomn for i in groups]

    for i in groups:
        keyboard.add(Callback(i.name, {"name": i.label}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Callback("Обе группы", {"name": "both"}), color=KeyboardButtonColor.POSITIVE)

    await bp.api.messages.edit(
        peer_id=event.object.user_id,
        user_id=event.object.user_id,
        message_id=msg_id,
        message="выбери",
        keyboard=keyboard.get_json()
    )


@bp.on.message_event(payload_map={"name": str})
async def set_group(event: GroupTypes.MessageEvent, scb: SCB):
    msg_id = scb.storage["message_ids"]
    subject = scb.storage["subject_to_fill"]
    if isinstance(subject, list):
        subject = subject[0]
    subject = scb.subjects[subject]
    payload = event.object.payload["name"]
    keyboard = Keyboard(inline=True)

    groups = await scb.subjects.find_groups(subject.label)

    chosen_group = scb.subjects[payload]

    for i in groups:
        if chosen_group.label == i.label:
            scb.storage["subject_to_fill"] = i.label
            scb.storage["readable_subject_name"] = i.nomn
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


@bp.on.private_message(state=HomeworkCreationStates.GET_SUBJECT)
async def get_subject(message: Message, scb: SCB):
    if message.payload:
        scb.storage["subject_to_fill"] = (subject := json.loads(message.payload)["subject"])
        subject = scb.subjects[subject]
        scb.storage["readable_subject_name"] = subject.nomn

    else:
        subject: SingleSubject = await scb.subjects.is_subject(message)
        if not subject:
            return "неизвестный предмет"

    #if subject.label == "physics":


    keyboard = NO_HOMEWORK_GIVEN
    if await scb.homework.get_last_homework(subject.label):
        keyboard = keyboard + LAST_HOMEWORK_KEYBOARD

    await message.answer(
        message="окей, предмет %s. введи текст или на кнопки нажми." % subject.nomn,
        keyboard=keyboard + BACK_TO_MENU
    )

    groups = await scb.subjects.find_groups(subject.label)
    logger.debug(groups)
    if groups:
        logger.debug("group detected")
        keyboard = Keyboard(inline=True)
        for i in groups:
            if i.lang_group == scb.user.lang_group or i.exam_group == scb.user.exam_group:
                scb.storage["subject_to_fill"] = i.label
                scb.storage["readable_subject_name"] = i.nomn
                color = KeyboardButtonColor.POSITIVE
            else:
                color = KeyboardButtonColor.PRIMARY
            keyboard.add(Callback(i.name, {"name": i.label}), color=color)
        sent = await message.answer(message="ок, выбери группу", keyboard=keyboard.get_json())
        scb.storage["message_ids"] = sent

    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.HOMEWORK_TEXT)
