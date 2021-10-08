from datetime import datetime
from vkbottle_overrides.bot import Message, rules

from keyboards import *
from vkbottle_overrides.bot import Blueprint
from utils import SCB
from utils import RegistrationStates

bp = Blueprint()
bp.name = "Registration"


@bp.on.message(FirstEntry=True)
async def first_entry_handler(message: Message, scb):
    await message.answer(scb.phrases.first_entry, keyboard=REGISTER_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_STATE)
    await scb.user.not_newbie_anymore()


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
    answer = scb.phrases.reg_grade
    grades = [grade.label for grade in await scb.grades.get_grades()]

    GRADE_KEYBOARD = Keyboard(one_time=False, inline=False)

    for grade in grades:
        GRADE_KEYBOARD.add(Text(grade, {"grade": grade}), row=4, color=KeyboardButtonColor.PRIMARY)

    if not message.client_info.keyboard:
        answer += ', '.join(grades)

    await message.answer(answer, keyboard=GRADE_KEYBOARD.get_json())
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)


@bp.on.message(state=RegistrationStates.GRADE_CHECK)
async def grade_check(message: Message, scb):
    """Проверка на существование класса."""
    answer = scb.phrases.wrong_grade
    keyboard = None

    if await scb.grades.is_grade(message.text):
        answer = scb.phrases.broadcast % message.text
        keyboard = YN_KEYBOARD
        scb.storage.set("grade", message.text)
        await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_STATE)

    await message.answer(answer, keyboard=keyboard)


@bp.on.message(rules.LevensteinRule("Да", 1), state=RegistrationStates.BROADCAST_STATE)
async def broadcast_enabled(message: Message, scb):
    """Если юзер согласился на рассылку."""
    await message.answer(scb.phrases.broadcast_type, keyboard=BROADCAST_TYPE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TYPE)


@bp.on.message(
    (
            rules.LevensteinRule("Время с конца последнего урока", 3),
            rules.VBMLRule("1"),
    ),
    state=RegistrationStates.BROADCAST_TYPE
)   # PHRASES IN RULES
async def broadcast_since(message: Message, scb):
    """Если юзер согласился на рассылку первого типа."""
    await message.answer(scb.phrases.broadcast_time_since, keyboard=TIME_SINCE_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_TIME, broadcast_type="since")


@bp.on.message(
    (
            rules.LevensteinRule("Фиксированное время", 3),
            rules.VBMLRule("2"),
    ),
    state=RegistrationStates.BROADCAST_TYPE
)   # PHRASES IN RULES
async def broadcast_fixed(message: Message, scb):
    """Если юзер согласился на рассылку второго типа."""
    await message.answer(scb.phrases.broadcast_time_fixed, keyboard=TIME_FIXED_KEYBOARD)
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
        return scb.phrases.broadcast_wrong_format

    await scb.user.register(grade)
    await scb.user.set_broadcast(broadcast_type=broadcast_type, time=message.text)
    await message.answer(scb.phrases.registration_passed.render(grade=grade, result=msg), keyboard=EMPTY_KEYBOARD)


@bp.on.message(rules.LevensteinRule("Нет", 3), state=RegistrationStates.BROADCAST_STATE)
async def broadcast_false(message: Message, scb):
    grade = scb.storage.get("grade")

    await message.answer(scb.phrases.registration_passed.render(grade=grade, result="нет"), keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.FINAL_STATE, broadcast=False)


@bp.on.message(state=RegistrationStates.BROADCAST_STATE)
async def broadcast_not_stated(message: Message, scb):
    """Заглушка. Если предудыщие хэндлеры не ответили, значит юзер прислал что-то непонятное вместо ответа."""
    await message.answer(scb.phrases.broadcast_not_stated)


@bp.on.message(NotRegistered=True)
async def registration_handler(message: Message, scb):
    await message.answer(scb.phrases.must_register,
                         keyboard=REGISTER_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_STATE)