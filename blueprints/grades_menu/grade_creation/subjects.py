from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD, EMPTY_KEYBOARD, LANGUAGES_KEYBOARD, Text
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules
from rules import IsMessageNotEmpty
import re
import pymorphy2

bp = Blueprint()
bp.name = "Subjects"
bp.labeler.auto_rules = [IsMessageNotEmpty.IsMessageNotEmpty()]


@bp.on.message(state=GradeCreationStates.SUBJECT_LANG)
async def subject_lang(message: Message, scb: SCB):
    if not message.text in scb.phrases.languages:
        return scb.phrases.grades.wrong_language
    info = scb.storage.get(message.peer_id)
    info["lang"] = message.text
    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.subject_label)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECT_LABEL)


@bp.on.message(text="Завершить", state=GradeCreationStates.SUBJECT_LABEL)
async def subjects_end(message: Message, scb: SCB):
    msg = scb.phrases.grades.input_subjects

    for language in scb.phrases.languages:
        LANGUAGES_KEYBOARD.add(Text(language), row=3)
        msg += f"-- {language}\n"

    await message.answer(msg, keyboard=EMPTY_KEYBOARD)  # PHRASES
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SCHEDULE)


@bp.on.message(state=GradeCreationStates.SUBJECT_LABEL)
async def subject_label(message: Message, scb: SCB):
    pattern = re.compile('[\W_]+')
    scrapped_label = pattern.sub('', message.text).lower()

    info = scb.storage.get(message.peer_id)
    info["subject_label"] = scrapped_label
    info["subjects"][scrapped_label] = {}
    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.subject_name)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECT_NAME)


@bp.on.message(state=GradeCreationStates.SUBJECT_NAME)
async def subject_name(message: Message, scb: SCB):
    morph = pymorphy2.MorphAnalyzer()
    subject = morph.parse(message.text)

    cases = {
        "nom": subject[0].inflect({"nomn"}).word,
        "gen": subject[0].inflect({"gent"}).word,
        "dat": subject[0].inflect({"datv"}).word,
        "acc": subject[0].inflect({"accs"}).word,
        "abl": subject[0].inflect({"ablt"}).word,
        "loc": subject[0].inflect({"loct"}).word
    }

    info = scb.storage.get(message.peer_id)
    label = info["subject_label"]
    print(info)
    info["subjects"][label]["cases"] = cases
    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.subject_shorts)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECT_SHORTS)


@bp.on.message(state=GradeCreationStates.SUBJECT_SHORTS)
async def subject_shorts(message: Message, scb: SCB):
    if not "," in message.text:
        return "пшел нах"

    shorts = [i.strip() for i in message.text.split(",")]

    info = scb.storage.get(message.peer_id)
    label = info["subject_label"]
    info["subjects"][label]["shorts"] = shorts
    scb.storage.set(message.peer_id, info)
    await message.answer(scb.phrases.grades.subject_emoji)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECT_EMOJI)


@bp.on.message(state=GradeCreationStates.SUBJECT_EMOJI)
async def subject_emoji(message: Message, scb: SCB):
    info = scb.storage.get(message.peer_id)
    label = info["subject_label"]
    info["subjects"][label]["emoji"] = message.text
    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.schedule % "понедельник", keyboard=EMPTY_KEYBOARD)  # PHRASES
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SUBJECT_LABEL)

