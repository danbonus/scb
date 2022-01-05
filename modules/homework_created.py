from keyboards.homework import HOMEWORK_KEYBOARD
from utils.args_object import SCB
from datetime import datetime


async def final(message, scb: SCB):
    records = await scb.homework.create(
        subjects=scb.storage["subject_to_fill"],
        homework=scb.storage["homework_text"],
        attachments=scb.storage["attachments"],
        to=scb.storage["deadline"],
        sender=scb.user.uid
    )
    days = scb.phrases.constants.days
    for record in records:
        await message.answer(
            "дз добавлено вся хуйня \nПредмет: %s\nДЗ: %s\nС какого числа: %s, %s\nДо какого числа: %s, %s" % (
                record["subject"],
                record["homework"],
                datetime.fromtimestamp(record["timestamp"]).strftime("%d.%m.%Y"),
                days[str(datetime.fromtimestamp(record["timestamp"]).weekday())].lower(),
                datetime.fromtimestamp(record["to"]).strftime("%d.%m.%Y"),
                days[str(datetime.fromtimestamp(record["to"]).weekday())].lower(),
            ),
            keyboard=HOMEWORK_KEYBOARD)
    for i in ["subject_to_fill", "homework_text", "attachments", "deadline"]:
        scb.storage.delete(i)
