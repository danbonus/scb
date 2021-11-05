from constants import HOMEWORK_OPERATIONS_KEYBOARD
from utils.args_object import SCB


async def final(message, scb: SCB):
    records = await scb.homework.create(
        subjects=scb.storage["subject_to_fill"],
        homework=scb.storage["homework_text"],
        attachments=scb.storage["attachments"],
        to=scb.storage["deadline"],
        sender=scb.user.uid
    )
    for record in records:
        await message.answer("дз добавлено вся хуйня \nПредмет: %s\nДЗ: %s\nДо какого числа: %s" % (
            record["subject"], record["homework"], record["to"]
        ), keyboard=HOMEWORK_OPERATIONS_KEYBOARD)
    for i in ["subject_to_fill", "homework_text", "attachments", "deadline"]:
        scb.storage.delete(i)
