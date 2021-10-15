from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD, FIRST_BELL, LANGUAGES_KEYBOARD, Text, EMPTY_KEYBOARD, BELLS_END
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Bells"


@bp.on.message(text=["0", "1"], state=GradeCreationStates.FIRST_BELL)
async def first_bell_input(message: Message, scb: SCB):
    print(scb.storage.get(message.peer_id))
    scb.storage.update(message.peer_id, first_bell=message.text)
    await message.answer(scb.phrases.grades.enter_bells % message.text, keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.BELLS)


@bp.on.message(state=GradeCreationStates.FIRST_BELL)
async def first_bell_wrong(message: Message, scb: SCB):
    return scb.phrases.grades.wrong_bell_format


@bp.on.message(text="Конец", state=GradeCreationStates.BELLS)
async def bells_input_end(message: Message, scb: SCB):
    info = scb.storage.get(message.peer_id)
    msg = scb.phrases.grades.bells_entered % info["label"]

    if not info["bells"]:
        return scb.phrases.grades.no_bells

    for lesson_number, bell in info["bells"].items():
        msg += f'{lesson_number}. {bell["start"]} - {bell["end"]}\n'

    msg += scb.phrases.grades.input_subjects

    for language in scb.phrases.languages:
        LANGUAGES_KEYBOARD.add(Text(language), row=3)
        msg += f"-- {language}\n"

    await message.answer(msg, keyboard=LANGUAGES_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECT_LANG)


@bp.on.message(state=GradeCreationStates.BELLS)
async def bells_input(message: Message, scb: SCB):
    try:
        lesson_start, lesson_end = [i.strip() for i in message.text.split("-")]
        scb.time.hm_format(lesson_start) or not(scb.time.hm_format(lesson_end))
    except ValueError:
        return scb.phrases.grades.wrong_bell_format

    info = scb.storage.get(message.peer_id)
    first_bell = info["first_bell"]

    bells_num = int(first_bell) + len(info["bells"])
    info["bells"][str(bells_num)] = {"start": lesson_start, "end": lesson_end}

    scb.storage.set(message.peer_id, info)
    await message.answer(scb.phrases.grades.bells_iter % (bells_num + 1), keyboard=BELLS_END)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.BELLS)
