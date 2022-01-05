from vkbottle import EMPTY_KEYBOARD

from constants.states import GradeCreationStates
from keyboards.misc import RETURN_KEYBOARD
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Bells"


@bp.on.private_message(text=["0", "1"], state=GradeCreationStates.FIRST_BELL)
async def first_bell_input(message: Message, scb: SCB):
    scb.storage["first_bell"] = message.text
    await message.answer(scb.phrases.grade_creation.enter_bells % message.text, keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.BELLS)


@bp.on.private_message(state=GradeCreationStates.FIRST_BELL)
async def first_bell_wrong(message: Message, scb: SCB):
    return scb.phrases.grade_creation.wrong_bell_format


@bp.on.private_message(state=GradeCreationStates.BELLS)
async def bells_input(message: Message, scb: SCB):
    msg = [i.split("-") for i in message.text.splitlines()]
    bells = {}
    info = scb.storage
    first_bell = info["first_bell"]

    try:
        for index, i in enumerate(msg):
            lesson_start, lesson_end = [i.strip() for i in i]
            scb.time.hm_format(lesson_start) or not(scb.time.hm_format(lesson_end))
            last_bell = str(index + int(first_bell))
            bells[last_bell] = {"start": lesson_start, "end": lesson_end}

    except ValueError:
        return scb.phrases.grade_creation.wrong_bell_format

    scb.storage["bells"] = bells
    scb.storage["subjects_chosen"] = []
    scb.storage["schedule"] = {}
    scb.storage["subjects"] = []
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SCHEDULE)
    #print(await bp.state_dispenser.get(message.peer_id))
    await message.answer(scb.phrases.grade_creation.schedule % scb.phrases.constants.days["0"].lower())

'''@bp.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)  # func=lambda e: e.object.payload== json.dumps({"easter": "беу)"}
async def easter(event: GroupTypes.MessageEvent, scb):
    print("EASTER!")
    await bp.api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=json.dumps({'type': "show_snackbar", "text": "беу)"})
    )'''