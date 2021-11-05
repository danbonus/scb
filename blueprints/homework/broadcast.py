from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import BroadcastStates
from constants.keyboards import RETURN_KEYBOARD, BROADCAST_TYPE_KEYBOARD, TIME_SINCE_KEYBOARD, TIME_FIXED_KEYBOARD, MENU_KEYBOARD, YN_KEYBOARD
from datetime import datetime
import json
from vkbottle import GroupEventType, GroupTypes
from rules.IsWriter import IsWriter
from logger import logger

bp = Blueprint()
bp.name = "Broadcast"


@bp.on.message(text="Рассылка")
async def broadcast(message: Message, scb: SCB):
    """Если юзер согласился на рассылку."""
    logger.critical(bp.handlers)
    await message.answer("ок да нет?", keyboard=YN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, BroadcastStates.ENABLE_BROADCAST)


@bp.on.message(text="Да", state=BroadcastStates.ENABLE_BROADCAST)
@bp.on.message(payload={"broadcast": True}, state=BroadcastStates.ENABLE_BROADCAST)
async def broadcast_enabled(message: Message, scb: SCB):
    await message.answer(scb.phrases.broadcast.type, keyboard=BROADCAST_TYPE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, BroadcastStates.BROADCAST_TYPE)


@bp.on.message(payload={"time": "since"}, state=BroadcastStates.BROADCAST_TYPE)
@bp.on.message(text=["Время с конца последнего урока", "1"],
               state=BroadcastStates.BROADCAST_TYPE)  # PHRASES IN RULES
async def broadcast_since(message: Message, scb: SCB):
    """Если юзер согласился на рассылку первого типа."""
    await message.answer(scb.phrases.broadcast.time_since, keyboard=TIME_SINCE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, BroadcastStates.BROADCAST_TIME, broadcast_type="since")


@bp.on.message(payload={"time": "fixed"}, state=BroadcastStates.BROADCAST_TYPE)
@bp.on.message(text=["Фиксированное время", "2"], state=BroadcastStates.BROADCAST_TYPE)  # PHRASES IN RULES
async def broadcast_fixed(message: Message, scb: SCB):
    """Если юзер согласился на рассылку второго типа."""
    await message.answer(scb.phrases.broadcast.time_fixed, keyboard=TIME_FIXED_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, BroadcastStates.BROADCAST_TIME, broadcast_type="fixed")


@bp.on.message(state=BroadcastStates.BROADCAST_TIME)
async def broadcast_final(message: Message, scb: SCB):
    """Проверка на соответствие формата даты, окончание регистрации."""
    broadcast_type = message.state_peer.payload["broadcast_type"]

    try:
        datetime.strptime(message.text, "%H:%M")
        msg = f"да, через {message.text} с конца уроков."

        if broadcast_type == "fixed":
            msg = f"да, в {message.text}"

        # await bp.state_dispenser.set(message.peer_id, RegistrationStates.FINAL_STATE)
    except ValueError:  # неправильный формат времени
        return scb.phrases.broadcast.wrong_format

    await scb.user.set_broadcast(type=broadcast_type, time=message.text)
    await message.answer(
        "окке гуд рассылка пройдена",
        keyboard=MENU_KEYBOARD
    )
    await bp.state_dispenser.delete(message.peer_id)


@bp.on.message(text="Нет", state=BroadcastStates.ENABLE_BROADCAST)
@bp.on.message(payload={"broadcast": True}, state=BroadcastStates.ENABLE_BROADCAST)
async def broadcast_not_enabled(message: Message, scb: SCB):
    await message.answer("на нет и суда нет", keyboard=MENU_KEYBOARD)
    await bp.state_dispenser.delete(message.peer_id)


@bp.on.message(state=[BroadcastStates.ENABLE_BROADCAST, BroadcastStates.BROADCAST_TYPE])
async def broadcast_not_stated(message: Message, scb: SCB):
    """Заглушка. Если предудыщие хэндлеры не ответили, значит юзер прислал что-то непонятное вместо ответа."""
    await message.answer(scb.phrases.broadcast.not_stated)
