from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import END_KEYBOARD, SUBJECTS_END_KEYBOARD, EMPTY_KEYBOARD, LANGUAGES_KEYBOARD, Text, iteration_keyboard
from constants.keyboards import RETURN_KEYBOARD, SUBJECTS_KEYBOARD, CREATE_SUBJECT_KEYBOARD, LANGUAGES_KEYBOARD, Text, EMPTY_KEYBOARD

from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules
from rules import IsMessageNotEmpty
import re
import pymorphy2
import json
from utils.api_test import Pagination
from vkbottle import Callback, GroupEventType, GroupTypes


bp = Blueprint()
bp.name = "Subjects!!!"
#bp.labeler.auto_rules = [IsMessageNotEmpty.IsMessageNotEmpty()]


'''@bp.on.message(text="Завершить", state=GradeCreationStates.SUBJECTS)
async def subjects_end(message: Message, scb: SCB):
    msg = "Предметы: \n"
    subjects = scb.storage["subjects_chosen"]
    for subject in subjects:
        msg += f"{subject.nomn}: {', '.join(subject.shorts)} \n"
      # PHRASES
    await message.answer(msg + "\n" + scb.phrases.grade_creation.schedule % "понедельник", keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SCHEDULE)


@bp.on.message(state=GradeCreationStates.SUBJECTS)
async def subjects_input(message: Message, scb: SCB):
    info = scb.storage
    message.text = message.text.lower()
    given_subject = await scb.subjects.is_subject(message)

    if given_subject:
        if given_subject in scb.storage["subjects_chosen"]:
            return "Этот предмет уже есть, ёпта"
        scb.storage["subjects_chosen"].append(given_subject)
    else:
        if 'last_msg' in scb.storage:
            return "Нет такого предмета, БЛЯ!"

    chosen_subjects = scb.storage["subjects_chosen"]
    print(scb.subjects.list)
    subjects = scb.subjects.list
    for i in scb.storage["subjects_chosen"]:
        subjects.pop(subjects.index(i))
    pagination = Pagination(subjects, 6, message.payload)
    page_subjects, page_keyboard = pagination.get()
    available_subjects = [i for i in page_subjects if i not in chosen_subjects]
    subjects_plain, keyboard = iteration_keyboard([subject.nomn for subject in available_subjects])
    print(chosen_subjects)
    msg = scb.phrases.grade_creation.subjects_entered + ', '.join([i.nomn for i in chosen_subjects]) + "\n\n" + scb.phrases.grade_creation.input_subjects.safe_substitute(subjects=subjects_plain)

    sent = await message.answer(msg, keyboard=CREATE_SUBJECT_KEYBOARD + keyboard + page_keyboard + RETURN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECTS)
    scb.storage["last_msg"] = sent
    scb.storage["last_msg_text"] = msg
    print(sent)


@bp.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_pagination(event: GroupTypes.MessageEvent, scb):
    if 'last_msg' not in scb.storage:
        await bp.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.peer_id,
            event_data=json.dumps({"type": "show_snackbar", "text": "Просрочено! Упс."})
        )
    else:
        subjects = scb.subjects.list
        for i in scb.storage["subjects_chosen"]:
            subjects.pop(subjects.index(i))
        pagination = Pagination(subjects, 6, event.object.payload)
        subjects, page_keyboard = pagination.get()
        subjects, keyboard = iteration_keyboard([subject.nomn for subject in subjects])
        print(event.object.conversation_message_id)
        print(event.object.payload)
        await bp.api.messages.edit(
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            message_id=scb.storage["last_msg"],
            message=scb.storage["last_msg_text"],
            keyboard=CREATE_SUBJECT_KEYBOARD + keyboard + page_keyboard + RETURN_KEYBOARD
        )
        await bp.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.peer_id
        )
'''
