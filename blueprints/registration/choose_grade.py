from vkbottle_overrides.bot import Message

from constants import *
from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants import RegistrationStates

bp = Blueprint()
bp.name = "Registration. Choose grade"


'''@bp.on.message(text=["Пройти регистрацию", "1"], NotRegistered=True, state=RegistrationStates.REGISTRATION_START)
async def reg_start(message: Message, scb: SCB):
    """Начало регистрации, выбор класса."""
    answer = scb.phrases.registration.reg_grade

    GRADE_KEYBOARD = Keyboard(one_time=False, inline=False)

    for grade in await scb.grades.list:
        GRADE_KEYBOARD.add(Text(grade.label, {"grade": grade.label}), row=4, color=KeyboardButtonColor.PRIMARY)

    if not message.client_info.keyboard:
        answer += ', '.join(await scb.grades.list)

    await message.answer(answer, keyboard=GRADE_KEYBOARD.get_json())
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)'''


@bp.on.message(state=RegistrationStates.GRADE_CHECK)
async def grade_check(message: Message, scb: SCB):
    """Проверка на существование класса."""
    answer = scb.phrases.registration.wrong_grade
    keyboard = None

    if await scb.grades.is_grade(message.text):
        answer = scb.phrases.broadcast.broadcast % message.text
        keyboard = YN_KEYBOARD
        scb.storage.set("grade", await scb.grades.get(message.text))
        await bp.state_dispenser.set(message.peer_id, RegistrationStates.BROADCAST_STATE)

    await message.answer(answer, keyboard=keyboard)
