from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
import datetime
from string import Template
from constants.states import EmulationStates
from constants.keyboards import RETURN_KEYBOARD, EMULATION_DAY_KEYBOARD
from rules.IsWriter import IsWriter
import json
from vkbottle.tools.dev_tools.loop_wrapper import LoopWrapper
from asyncio import create_task


bp = Blueprint()
bp.name = "Emulation"


@bp.on.message(text="Эмуляция")
@bp.on.message(payload={"cmd": "emulation"})
async def emulation(message: Message, scb: SCB):
    await bp.state_dispenser.set(message.peer_id, EmulationStates.EMULATION_DAY)
    await message.answer(
        message="окей, выбери день",
        keyboard=EMULATION_DAY_KEYBOARD + RETURN_KEYBOARD
    )


@bp.on.message(payload_map={"emulation": str}, state=EmulationStates.EMULATION_DAY)
@bp.on.message(text=["1", "2"], state=EmulationStates.EMULATION_DAY)
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
    await message.answer(message="окей, вводи дату в формате 27.01.2021", keyboard=RETURN_KEYBOARD)


@bp.on.message(state=EmulationStates.EMULATION_INPUT)
async def emulation_input(message: Message, scb: SCB):
    date = message.text
    if message.state_peer.payload["day"] == "from":
        scb.storage["emulation_date"] = date
    else:
        scb.storage["emulation_date"] = scb.time.get_yesterday(date).strftime("%d.%m.%Y")

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(message="эмуляция активна. пиши дз. отключится через 20 минут.", keyboard=RETURN_KEYBOARD)
    bp.loop_wrapper.create_timer(emulation_timer, minutes=20, message=message, scb=scb)


async def emulation_timer(message: Message, scb: SCB):
    await message.answer("отключено!")
    scb.storage.delete("emulation_date")


@bp.on.message(text="⛔ Отключить эмуляцию")
async def off_emulation(message: Message, scb: SCB):
    scb.storage.delete("emulation_date")
    return "эмуляция отключена"
