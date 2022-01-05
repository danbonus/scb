import json

from constants import RegistrationStates
from keyboards.groups import groups_iteration
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Registration. Choose grade"


@bp.on.private_message(state=RegistrationStates.GRADE_CHECK)
async def grade_check(message: Message, scb: SCB):
    """Проверка на существование класса."""
    payload = json.loads(message.payload)
    if payload:
        grade = await scb.grades.get(payload["grade"])
    else:
        grade = await scb.grades.is_grade(message.text)

    if not grade:
        return scb.phrases.registration.wrong_grade

    answer = "ок класс указан вся хуйня теперь укажи группу\n\n"

    #answer += scb.phrases.broadcast.broadcast % message.text
    plain, keyboard = groups_iteration(grade.lang_groups)

    await message.answer(message=answer, keyboard=keyboard)
    scb.storage.set("grade", grade)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GET_LANG_GROUP)
