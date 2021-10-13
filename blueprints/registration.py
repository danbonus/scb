from datetime import datetime
from vkbottle_overrides.bot import Message, rules

from keyboards import *
from vkbottle_overrides.bot import Blueprint
from utils import SCB
from utils import RegistrationStates

bp = Blueprint()
bp.name = "Registration"


@bp.on.message(FirstEntry=True)
async def first_entry_handler(message: Message, scb: SCB):
    await message.answer(scb.phrases.registration.first_entry, keyboard=REGISTER_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_STATE)


@bp.on.message(
    (
            rules.PayloadRule({"reg": "start"}),
            rules.LevensteinRule("Пройти регистрацию", 3),
            rules.VBMLRule("1"),
     ),
    NotRegistered=True,
    state=RegistrationStates.GRADE_STATE)
async def reg_grade(message: Message, scb: SCB):
    """Начало регистрации, выбор класса."""
    answer = scb.phrases.grades.reg

    GRADE_KEYBOARD = Keyboard(one_time=False, inline=False)

    for grade in await scb.grades.list:
        GRADE_KEYBOARD.add(Text(grade.label, {"grade": grade.label}), row=4, color=KeyboardButtonColor.PRIMARY)

    if not message.client_info.keyboard:
        answer += ', '.join(await scb.grades.list)

    await message.answer(answer, keyboard=GRADE_KEYBOARD.get_json())
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)


@bp.on.message(state=RegistrationStates.GRADE_CHECK)
async def grade_check(message: Message, scb: SCB):
    """Проверка на существование класса."""
    answer = scb.phrases.grades.wrong
    keyboard = None

    if await scb.grades.is_grade(message.text):
        answer = scb.phrases.broadcast.broadcast % message.text
        keyboard = YN_KEYBOARD
        scb.storage.set("grade", await scb.grades.get(message.text))
        await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_STATE)

    await message.answer(answer, keyboard=keyboard)


@bp.on.message(rules.LevensteinRule("Да", 1), state=RegistrationStates.BROADCAST_STATE)
async def broadcast_enabled(message: Message, scb: SCB):
    """Если юзер согласился на рассылку."""
    await message.answer(scb.phrases.broadcast.type, keyboard=BROADCAST_TYPE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TYPE)


@bp.on.message(
    (
            rules.LevensteinRule("Время с конца последнего урока", 3),
            rules.VBMLRule("1"),
    ),
    state=RegistrationStates.BROADCAST_TYPE
)   # PHRASES IN RULES
async def broadcast_since(message: Message, scb: SCB):
    """Если юзер согласился на рассылку первого типа."""
    await message.answer(scb.phrases.broadcast.time_since, keyboard=TIME_SINCE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TIME, broadcast_type="since")


@bp.on.message(
    (
            rules.LevensteinRule("Фиксированное время", 3),
            rules.VBMLRule("2"),
    ),
    state=RegistrationStates.BROADCAST_TYPE
)   # PHRASES IN RULES
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
        keyboard=EMPTY_KEYBOARD
    )
    await scb.user.register(grade.id)


@bp.on.message(rules.LevensteinRule("Нет", 3), state=RegistrationStates.BROADCAST_STATE)
async def broadcast_false(message: Message, scb: SCB):
    grade = scb.storage.get("grade")

    await message.answer(
        scb.phrases.registration.passed.substitute(grade=grade.label, result="нет"),
        keyboard=EMPTY_KEYBOARD
    )
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.FINAL_STATE, broadcast=False)
    await scb.user.register(grade.id)


@bp.on.message(state=RegistrationStates.BROADCAST_STATE)
async def broadcast_not_stated(message: Message, scb: SCB):
    """Заглушка. Если предудыщие хэндлеры не ответили, значит юзер прислал что-то непонятное вместо ответа."""
    await message.answer(scb.phrases.broadcast.not_stated)


@bp.on.message(NotRegistered=True)
async def registration_handler(message: Message, scb: SCB):
    await message.answer(scb.phrases.registration.must_register,
                         keyboard=REGISTER_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_STATE)
