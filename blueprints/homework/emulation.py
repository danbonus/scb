import json
from datetime import datetime

from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import Message

from constants.states import EmulationStates
from keyboards.emulation import EMULATION_DAY_KEYBOARD, CANCEL_EMULATION_KEYBOARD
from keyboards.misc import RETURN_KEYBOARD, BACK_TO_MENU
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Emulation"


@bp.on.private_message(text="Эмуляция")
@bp.on.private_message(payload={"cmd": "emulation"})
async def emulation(message: Message, scb: SCB):
    await bp.state_dispenser.set(message.peer_id, EmulationStates.EMULATION_DAY)

    if "emulation_date" in scb.storage:
        keyboard = EMULATION_DAY_KEYBOARD + CANCEL_EMULATION_KEYBOARD + BACK_TO_MENU
    else:
        keyboard = EMULATION_DAY_KEYBOARD + BACK_TO_MENU

    await message.answer(
        message="окей, выбери день",
        keyboard=keyboard
    )


@bp.on.private_message(payload_map={"emulation": str}, state=EmulationStates.EMULATION_DAY)
@bp.on.private_message(text=["1", "2"], state=EmulationStates.EMULATION_DAY)
async def emulation_input(message: Message, scb: SCB):
    if message.payload:
        day = json.loads(message.payload)["emulation"]
    elif message.text == "1":
        day = "from"
    elif message.text == "2":
        day = "to"
    else:
        return "что"

    await bp.state_dispenser.set(
        message.peer_id, EmulationStates.EMULATION_INPUT,
        day=day
    )
    await message.answer(message="окей, вводи дату в формате 27.01.2021", keyboard=BACK_TO_MENU)


@bp.on.private_message(state=EmulationStates.EMULATION_INPUT)
async def emulation_input(message: Message, scb: SCB):
    date = message.text
    if message.state_peer.payload["day"] == "from":
        scb.storage["emulation_date"] = datetime.strptime(date, "%d.%m.%Y").replace(hour=11)
    else:
        scb.storage["emulation_date"] = scb.time.get_yesterday(date).replace(hour=11)

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(message="эмуляция активна. пиши дз. отключится через 20 минут.", keyboard=BACK_TO_MENU)
    bp.loop_wrapper.create_timer(emulation_timer, minutes=20, message=message, scb=scb)


async def emulation_timer(message: Message, scb: SCB):
    await message.answer("отключено!")
    scb.storage.delete("emulation_date")


@bp.on.private_message(text="⛔ Отключить эмуляцию")
async def off_emulation(message: Message, scb: SCB):
    scb.storage.delete("emulation_date")
    await message.answer(message="эмуляция отключена", keyboard=BACK_TO_MENU)
