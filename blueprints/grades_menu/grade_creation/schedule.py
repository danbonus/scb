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
    info = scb.storage.get(message.peer_id)

    schedule_dict = await get_schedule(message.text)

    records_count = len(info["schedule"])
    info["schedule"][str(records_count)] = schedule_dict
    records_count += 1

    if records_count == 5:
        await bp.state_dispenser.set(message.peer_id, GradeCreationStates.END)

    scb.storage.set(message.peer_id, info)

    await message.answer(scb.phrases.grades.schedule_iter % scb.phrases.constants.days_acc[str(records_count)].lower())


@bp.on.message(state=GradeCreationStates.END)
async def end(message: Message, scb: SCB):
    info = scb.storage.get(message.peer_id)

    schedule_dict = await get_schedule(message.text)

    info["schedule"]["5"] = schedule_dict
    scb.storage.set(message.peer_id, info)
    msg = "Расписание:\n\n"
    for day, day_schedule in info["schedule"].items():
        msg += "%s:\n" % scb.phrases.constants.days[day]
        for lesson_number, lesson in day_schedule.items():
            msg += "%s. %s\n" % (lesson_number, lesson)
        msg += "\n\n"

    await scb.grades.create(
        label=info["label"],
        album_id=info["album_id"],
        bells=info["bells"],
        subjects={
            info["lang"]: info["subjects"]
        },
        schedule=info["schedule"]
    )
    await message.answer(msg)
    await bp.state_dispenser.set(message.peer_id, GradeCreationStates.SCHEDULE)


async def get_schedule(text):
    msg = text.splitlines()
    schedule_dict = {}  # 0. География

    for i in msg:
        lesson_number, subject = i.split(".")
        schedule_dict[lesson_number] = subject  # label

    return schedule_dict
