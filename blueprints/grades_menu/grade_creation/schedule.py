from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.states import GradeCreationStates
from vkbottle_overrides.bot import Message
from rules import IsMessageNotEmpty

bp = Blueprint()
bp.name = "Grade Schedule"


bp.labeler.auto_rules = [IsMessageNotEmpty.IsMessageNotEmpty()]


@bp.on.message(state=GradeCreationStates.SCHEDULE)
async def schedule(message: Message, scb: SCB):
    try:
        schedule_dict = await get_schedule(message.text, scb)
    except ValueError:
        return scb.phrases.grade_creation.wrong_bell_format

    records_count = len(scb.storage["schedule"])
    scb.storage["schedule"][str(records_count)] = schedule_dict
    records_count += 1

    if records_count == 5:
        await bp.state_dispenser.set(message.peer_id, GradeCreationStates.END)

    await message.answer(scb.phrases.grade_creation.schedule_iter % scb.phrases.constants.days_acc[str(records_count)].lower())


@bp.on.message(state=GradeCreationStates.END)
async def end(message: Message, scb: SCB):

    schedule_dict = await get_schedule(message.text, scb)

    scb.storage["schedule"]["5"] = schedule_dict

    msg = "Расписание:\n\n"
    for day, day_schedule in scb.storage["schedule"].items():
        msg += "%s:\n" % scb.phrases.constants.days[day]
        for lesson_number, lesson in day_schedule.items():
            msg += "%s. [%s] %s\n" % (lesson_number, lesson["room"], scb.subjects[lesson["subject"]].nomn)
        msg += "\n\n"

    (await scb.grades).create(
        label=scb.storage["label"],
        album_id=scb.storage["album_id"],
        bells=scb.storage["bells"],
        subjects=scb.storage["subjects"],
        schedule=scb.storage["schedule"]
    )
    await message.answer(msg)
    await bp.state_dispenser.delete(message.peer_id)


async def get_schedule(text, scb: SCB):
    msg = text.splitlines()
    schedule_dict = {}  # 0. География
    grade_subjects = scb.storage["subjects"]

    for i in msg:
        lesson_number, subject_and_room = i.split(".")
        room, subject = subject_and_room.split("]")
        room = room.split("[")[1]
        given_subject = await scb.subjects.is_subject(Message(subject))
        schedule_dict[lesson_number] = {}
        schedule_dict[lesson_number]["room"] = room.strip()
        schedule_dict[lesson_number]["bell"] = lesson_number

        if given_subject:
            schedule_dict[lesson_number]["subject"] = given_subject.label
            if given_subject.label not in grade_subjects:
                grade_subjects.append(given_subject.label)
        else:
            subject = await scb.subjects.create(
                label=subject,
                name=subject,
                shorts=[subject],
                emoji="[?]"
            )
            if subject["label"] not in grade_subjects:
                grade_subjects.append(subject["label"])
            schedule_dict[lesson_number]["subject"] = subject["label"]  # label

    return schedule_dict


class Message:
    # заглушка
    def __init__(self, text):
        self.text = text.lower().strip()
