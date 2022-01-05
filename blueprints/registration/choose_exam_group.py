
import json

from constants import RegistrationStates, BroadcastStates
from keyboards.misc import YN_KEYBOARD
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Registration. Choose exam group"


@bp.on.private_message(state=RegistrationStates.GET_EXAM_GROUP)
async def exam_group_check(message: Message, scb: SCB):
    """Проверка на существование класса."""
    payload = json.loads(message.payload)
    if payload:
        group = payload["group"]
    else:
        group = (await scb.grades.is_group(scb.grades.exam_groups, message.text)).num

    if not group:
        return scb.phrases.registration.wrong_grade

    await message.answer("Рассыл очка. Надо?", keyboard=YN_KEYBOARD)

    scb.storage.set("exam_group", group)

    await bp.state_dispenser.set(message.peer_id, BroadcastStates.ENABLE_BROADCAST)
    await scb.user.register(scb.storage["grade"].id, scb.storage["lang_group"], scb.storage["exam_group"])
