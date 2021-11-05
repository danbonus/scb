from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates
from constants.keyboards import HOMEWORK_CREATION_KEYBOARD
from vkbottle_overrides.bot import rules

bp = Blueprint()
bp.name = "HW ADD: text"


@bp.on.message(
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
    scb.storage["homework_text"] = last_record.homework
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.OPTIONAL)

    await message.answer("окей, прошлое дз. пришли картинки или нажми завершить", keyboard=HOMEWORK_CREATION_KEYBOARD)


@bp.on.message(state=HomeworkCreationStates.HOMEWORK_TEXT)
async def homework_text(message: Message, scb: SCB):
    if not message.text:
        return "где текст"

    if not message.text.endswith("."):
        message.text += "."
    if message.text[0].isupper():
        message.text = message.text[0].lower() + message.text[1:]

    scb.storage["homework_text"] = message.text
    await bp.state_dispenser.set(message.peer_id, HomeworkCreationStates.OPTIONAL)

    await message.answer("окей, текст добавил. пришли картинки или дедлайн или нажми завершить", keyboard=HOMEWORK_CREATION_KEYBOARD)