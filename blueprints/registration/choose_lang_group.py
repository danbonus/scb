
import json

from constants import RegistrationStates
from keyboards.groups import groups_iteration
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Registration. Choose lang group"


@bp.on.private_message(state=RegistrationStates.GET_LANG_GROUP)
async def lang_group_check(message: Message, scb: SCB):
    payload = json.loads(message.payload)
    if payload:
        group = payload["group"]
    else:
        group = (await scb.grades.is_group(scb.grades.lang_groups, message.text)).num

    if not group:
        return scb.phrases.registration.wrong_grade

    grade = scb.storage["grade"]
    plain, keyboard = groups_iteration(grade.exam_groups)
    await message.answer("Gud. Group: %s" % group, keyboard=keyboard)

    scb.storage.set("lang_group", group)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GET_EXAM_GROUP)
