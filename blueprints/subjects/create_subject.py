from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import END_KEYBOARD, SUBJECTS_END_KEYBOARD, EMPTY_KEYBOARD, LANGUAGES_KEYBOARD, Text
from constants.keyboards import RETURN_KEYBOARD, SUBJECTS_KEYBOARD, CREATE_SUBJECT_KEYBOARD, LANGUAGES_KEYBOARD, Text, EMPTY_KEYBOARD

from constants.states import GradesMenuStates, SubjectCreationStates
from vkbottle_overrides.bot import Message, rules
from rules import IsMessageNotEmpty
import re
import pymorphy2

bp = Blueprint()
bp.name = "Subjects"
bp.labeler.auto_rules = [IsMessageNotEmpty.IsMessageNotEmpty()]


@bp.on.message(state=SubjectCreationStates.SUBJECT_LANG)
async def subject_lang(message: Message, scb: SCB):
    if not message.text in scb.phrases.languages:
        return scb.phrases.grade_creation.wrong_language

    scb.storage["lang"] = message.text

    await message.answer(scb.phrases.grade_creation.subject_label)
    await bp.state_dispenser.set(message.peer_id, SubjectCreationStates.SUBJECT_LABEL)


@bp.on.message(state=SubjectCreationStates.SUBJECT_LABEL)
async def subject_label(message: Message, scb: SCB):
    pattern = re.compile('[\W_]+')
    scrapped_label = pattern.sub('', message.text).lower()

    scb.storage["subject_label"] = scrapped_label
    scb.storage["subjects"][scrapped_label] = {}

    await message.answer(scb.phrases.grade_creation.subject_name)
    await bp.state_dispenser.set(message.peer_id, SubjectCreationStates.SUBJECT_NAME)


@bp.on.message(state=SubjectCreationStates.SUBJECT_NAME)
async def subject_name(message: Message, scb: SCB):
    cases = {}
    is_russian = re.compile(r'[а-яА-ЯёЁ]')
    if is_russian.match(message.text):
        morph = pymorphy2.MorphAnalyzer()
        subject = morph.parse(message.text)
        for i in ["nomn", "gent", "datv", "accs", "ablt", "loct"]:
            cases[i] = subject[0].inflect({i}).word
    else:
        for i in ["nomn", "gent", "datv", "accs", "ablt", "loct"]:
            cases[i] = message.text

    label = scb.storage["subject_label"]
    scb.storage["subjects"][label]["cases"] = cases

    await message.answer(scb.phrases.grade_creation.subject_shorts)
    await bp.state_dispenser.set(message.peer_id, SubjectCreationStates.SUBJECT_SHORTS)


@bp.on.message(state=SubjectCreationStates.SUBJECT_SHORTS)
async def subject_shorts(message: Message, scb: SCB):
    if not "," in message.text:
        return "пшел нах"

    shorts = [i.strip() for i in message.text.split(",")]

    label = scb.storage["subject_label"]
    scb.storage["subjects"][label]["shorts"] = shorts
    await message.answer(scb.phrases.grade_creation.subject_emoji)
    await bp.state_dispenser.set(message.peer_id, SubjectCreationStates.SUBJECT_EMOJI)


@bp.on.message(state=SubjectCreationStates.SUBJECT_EMOJI)
async def subject_emoji(message: Message, scb: SCB):
    label = scb.storage["subject_label"]
    scb.storage["subjects"][label]["emoji"] = message.text

    await message.answer(scb.phrases.grade_creation.new_subject, keyboard=END_KEYBOARD)  # PHRASES
    await bp.state_dispenser.set(message.peer_id, SubjectCreationStates.SUBJECT_LABEL)
