from datetime import datetime
from vkbottle_overrides.bot import Message

from constants import *
from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants import RegistrationStates

bp = Blueprint()
bp.name = "Registration. Broadcast"


@bp.on.message(text="Да", state=RegistrationStates.BROADCAST_STATE)
async def broadcast_enabled(message: Message, scb: SCB):
    """Если юзер согласился на рассылку."""
    await message.answer(scb.phrases.broadcast.type, keyboard=BROADCAST_TYPE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TYPE)


@bp.on.message(text=["Время с конца последнего урока", "1"],
               state=RegistrationStates.BROADCAST_TYPE)  # PHRASES IN RULES
async def broadcast_since(message: Message, scb: SCB):
    """Если юзер согласился на рассылку первого типа."""
    await message.answer(scb.phrases.broadcast.time_since, keyboard=TIME_SINCE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TIME, broadcast_type="since")


@bp.on.message(text=["Фиксированное время", "2"], state=RegistrationStates.BROADCAST_TYPE)  # PHRASES IN RULES
async def broadcast_fixed(message: Message, scb: SCB):
    """Если юзер согласился на рассылку второго типа."""
    await message.answer(scb.phrases.broadcast.time_fixed, keyboard=TIME_FIXED_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TIME, broadcast_type="fixed")


@bp.on.message(state=RegistrationStates.BROADCAST_TIME)
async def broadcast_final(message: Message, scb: SCB):
    """Проверка на соответствие формата даты, окончание регистрации."""
    grade = scb.storage.get("grade")
    broadcast_type = message.state_peer.payload["broadcast_type"]

    try:
        datetime.strptime(message.text, "%H:%M")
        msg = f"да, через {message.text} с конца уроков."

        if broadcast_type == "fixed":
            msg = f"да, в {message.text}"

        await bp.state_dispenser.set(message.peer_id, RegistrationStates.FINAL_STATE)
    except ValueError:  # неправильный формат времени
        return scb.phrases.broadcast.wrong_format

    await scb.user.set_broadcast(subscriber=True, type=broadcast_type, time=message.text)
    await message.answer(
        scb.phrases.registration.passed.substitute(grade=grade.label, result=msg),
        keyboard=MENU_KEYBOARD
    )
    await scb.user.register(grade.label)


@bp.on.message(text=["Нет"], state=RegistrationStates.BROADCAST_STATE)
async def broadcast_false(message: Message, scb: SCB):
    grade = scb.storage.get("grade")

    await message.answer(
        scb.phrases.registration.passed.substitute(grade=grade.label, result="нет"),
        keyboard=MENU_KEYBOARD
    )
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.FINAL_STATE, broadcast=False)
    await scb.user.register(grade.label)


@bp.on.message(state=RegistrationStates.BROADCAST_STATE)
async def broadcast_not_stated(message: Message, scb: SCB):
    """Заглушка. Если предудыщие хэндлеры не ответили, значит юзер прислал что-то непонятное вместо ответа."""
    await message.answer(scb.phrases.broadcast.not_stated)