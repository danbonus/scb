from blueprints.homework.homework import get_homework
from logger import logger
from utils.args_object import SCB
from vkbottle.tools.dev_tools.mini_types.bot.message import message_min
from vkbottle.bot import Message


async def update_homework(message: Message, scb: SCB):
    users = await scb.many_users.get_many("registered", True)
    logger.debug(users)
    homework_update = f"\n\n🔄 | Домашнее задание было обновлено в {scb.time.get_today().strftime('%H:%M %d.%m.%Y')}"
    writer_message = "Обновляю домашку у юзеров... \n\n"
    sent = await message.answer(message=writer_message)
    for i in users:
        if i.uid == message.from_id:
            continue
        logger.debug("Iterating over users: %s" % i.uid)
        requests = await scb.requests.get_last_handler_by_label(i.uid, ["homework", "homework_final"])
        logger.debug(requests)
        for request in await scb.homework.get_last_homework_requests(requests):
            event = message_min(request.event, scb.api.api)
            user_scb = await SCB(event)
            msg, attachments = await get_homework(user_scb, send=False)
            msg_id = request.record["answered_message_id"]

            try:
                await scb.api.api.messages.edit(
                    peer_id=i.uid,
                    message_id=msg_id,
                    message=msg + homework_update,
                    attachment=attachments
                )
                writer_message += f"✔ | [id{i.uid}|{i.last_name} {i.first_name}]\n"

            except:
                writer_message += f"❌ | [id{i.uid}|{i.last_name} {i.first_name}]\n"

            await message.ctx_api.messages.edit(
                peer_id=message.from_id,
                message=writer_message,
                message_id=sent
            )
    writer_message += "\nКонец!"
    await message.ctx_api.messages.edit(
        peer_id=message.from_id,
        message=writer_message,
        message_id=sent
    )