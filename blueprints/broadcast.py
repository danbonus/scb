import json

from datetime import datetime
from vkbottle.bot import Message

from constants.states import BroadcastStates
from keyboards.broadcast import DISABLE_BROADCAST, BROADCAST_TIME_KEYBOARD
from keyboards.misc import YN_KEYBOARD, BACK_TO_MENU
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Broadcast"


@bp.on.private_message(payload={"cmd": "broadcast"})
@bp.on.private_message(text="Рассылка")
async def broadcast(message: Message, scb: SCB):
    """Если юзер согласился на рассылку."""
    if scb.user.is_broadcast_subscriber:
        msg = "да, ты подписан на рассылку. \nвремя рассылки: через %s после конца учебного дня." % scb.user.broadcast_time
        await message.answer(message=msg, keyboard=DISABLE_BROADCAST)
        return

    await message.answer("ок да нет?", keyboard=YN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, BroadcastStates.ENABLE_BROADCAST)


@bp.on.private_message(payload={"cmd": "disable_broadcast"})
async def disable_broadcast(message: Message, scb: SCB):
    await scb.user.set_broadcast(False, None)
    await message.answer(message="окей", keyboard=BACK_TO_MENU)


@bp.on.private_message(text="Да", state=BroadcastStates.ENABLE_BROADCAST)
@bp.on.private_message(payload={"broadcast": True}, state=BroadcastStates.ENABLE_BROADCAST)
async def broadcast_enabled(message: Message, scb: SCB):
    await message.answer("выбери время", keyboard=BROADCAST_TIME_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, BroadcastStates.BROADCAST_TIME)


@bp.on.private_message(state=BroadcastStates.BROADCAST_TIME)
async def broadcast_final(message: Message, scb: SCB):
    """Проверка на соответствие формата даты, окончание регистрации."""
    payload = json.loads(message.payload)
    if payload:
        time = payload["broadcast_time"]
    else:
        try:
            datetime.strptime(message.text, "%H:%M")
            msg = f"да, через {message.text} с конца уроков."
            time = message.text
        except ValueError:  # неправильный формат времени
            return scb.phrases.broadcast.wrong_format

    await message.answer(
        "окке гуд рассылка пройдена",
        keyboard=BACK_TO_MENU
    )
    await scb.user.set_broadcast(True, time)
    await bp.state_dispenser.delete(message.peer_id)


@bp.on.private_message(text="Нет", state=BroadcastStates.ENABLE_BROADCAST)
@bp.on.private_message(payload={"broadcast": True}, state=BroadcastStates.ENABLE_BROADCAST)
async def broadcast_not_enabled(message: Message, scb: SCB):
    await message.answer("на нет и суда нет", keyboard=BACK_TO_MENU)
    await bp.state_dispenser.delete(message.peer_id)


@bp.on.private_message(state=BroadcastStates.ENABLE_BROADCAST)
async def broadcast_not_stated(message: Message, scb: SCB):
    """Заглушка. Если предудыщие хэндлеры не ответили, значит юзер прислал что-то непонятное вместо ответа."""
    await message.answer(scb.phrases.broadcast.not_stated)
