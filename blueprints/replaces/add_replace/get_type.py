from vkbottle.bot import Message

from constants.states import ReplaceCreationStates
from enums.replaces import Replaces
from keyboards.misc import END_KEYBOARD, EMPTY_KEYBOARD, BACK_TO_MENU
from rules.IsWriter import IsWriter
from utils.api_test import Pagination
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from modules.add_homework import get_subjects
from keyboards.subjects import subjects_iteration, subjects_to_delete_iteration


bp = Blueprint()
bp.name = "Replace creation: GET_TYPE "
bp.labeler.auto_rules.append(IsWriter())


@bp.on.private_message(payload={"replace_type": Replaces.no_lesson}, state=ReplaceCreationStates.GET_TYPE)
@bp.on.private_message(text="Нет урока", state=ReplaceCreationStates.GET_TYPE)
async def add_homework(message: Message, scb: SCB):
    scb.storage["replace_type"] = Replaces.no_lesson
    sent = await message.answer(
        "ок урока нет. можешь написать почему либо завершить",
        keyboard=END_KEYBOARD
    )
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_TEXT)


@bp.on.private_message(payload={"replace_type": Replaces.lesson_changed}, state=ReplaceCreationStates.GET_TYPE)
@bp.on.private_message(text="Другой урок", state=ReplaceCreationStates.GET_TYPE)
async def add_homework(message: Message, scb: SCB):
    scb.storage["replace_type"] = Replaces.lesson_changed
    '''grade_subjects = scb.subjects.grades_subjects
    pagination = Pagination(grade_subjects, 10, None, inline=False)
    page_subjects, page_keyboard = pagination.get()
    subjects_plain, keyboard = subjects_iteration(page_subjects, row=2)'''
    keyboard = await get_subjects(scb, None, skip_filled=False, skip_foreign_groups=False)
    scb.storage["skip_filled"] = False
    scb.storage["skip_foreign_groups"] = False
    sent = await message.answer("ок другой урок. какой? выбери на клаве либо сам введи, похуй", keyboard=keyboard + BACK_TO_MENU)
    scb.storage["message_ids"] = sent
    scb.storage["message_text"] = "📗 | Выбери предмет"
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_TEXT)


@bp.on.private_message(payload={"replace_type": Replaces.teacher_changed}, state=ReplaceCreationStates.GET_TYPE)
@bp.on.private_message(text="Замещение", state=ReplaceCreationStates.GET_TYPE)
async def add_homework(message: Message, scb: SCB):
    scb.storage["replace_type"] = Replaces.teacher_changed
    print("BEU")
    sent = await message.answer("ок замещение. кто замещает?", keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_TEXT)


@bp.on.private_message(payload={"replace_type": Replaces.room_changed}, state=ReplaceCreationStates.GET_TYPE)
@bp.on.private_message(text="Другой кабинет", state=ReplaceCreationStates.GET_TYPE)
async def add_homework(message: Message, scb: SCB):
    scb.storage["replace_type"] = Replaces.room_changed
    sent = await message.answer("ок другой каб. какой?", keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, ReplaceCreationStates.GET_TEXT)

