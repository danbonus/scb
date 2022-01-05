from vkbottle.bot import Message

from constants.states import HomeworkCreationStates
from keyboards.homework import DEADLINE_OR_FINISH
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import rules

bp = Blueprint()
bp.name = "HW ADD: text"


@bp.on.private_message(
    (
            rules.VBMLRule("прошлое дз"),
            rules.PayloadRule({'last_hw': True})
    ),
    state=HomeworkCreationStates.HOMEWORK_TEXT
)
async def last_homework(message: Message, scb: SCB):
    last_record = await scb.homework.get_last_homework(scb.storage["subject_to_fill"])
    if not last_record:
        return "нет еще прошлых записей куда гонишь"

    await message.answer("окей, прошлое дз. пришли картинки или нажми завершить", keyboard=DEADLINE_OR_FINISH)
    scb.storage["homework_text"] = last_record.homework
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.OPTIONAL)


@bp.on.private_message(
    (
            rules.VBMLRule("ничего"),
            rules.PayloadRule({'no_homework_given': True})
    ),
    state=HomeworkCreationStates.HOMEWORK_TEXT
)
async def no_homework_given(message: Message, scb: SCB):
    await message.answer("охуенчик, нихуя хуйня не задано. пришли картинки-хуинки или нажми завершить-хуержить", keyboard=DEADLINE_OR_FINISH)
    scb.storage["homework_text"] = "ничего."
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.OPTIONAL)


@bp.on.private_message(state=HomeworkCreationStates.HOMEWORK_TEXT)
async def homework_text(message: Message, scb: SCB):
    if not message.text:
        return "где текст"

    await message.answer("окей, текст добавил. пришли картинки или дедлайн или нажми завершить", keyboard=DEADLINE_OR_FINISH)

    text = await scb.utils.process_text(message.text)

    scb.storage["homework_text"] = text
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.OPTIONAL)
