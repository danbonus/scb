from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import HomeworkCreationStates
from vkbottle.http import ManySessionManager
from vkbottle import PhotoToAlbumUploader
from asyncio import gather
from logger import logger

bp = Blueprint()
bp.name = "HW ADD: attachments"


@bp.on.message(
    func=lambda message: len(message.get_photo_attachments()) > 0,
    state=[HomeworkCreationStates.OPTIONAL, HomeworkCreationStates.HOMEWORK_TEXT],
    blocking=False
)
async def homework_attachments(message: Message, scb: SCB):
    scb.storage["attachments"] = []
    attachments_list = []
    tasks = []

    msg = await bp.api.messages.get_by_conversation_message_id(
        peer_id=message.peer_id,
        conversation_message_ids=[message.conversation_message_id]
    )

    attachments = msg.items[0].get_photo_attachments()

    sent = await message.answer("🕘 | Добавляются %s картинок..." % len(attachments))
    logger.debug("New attachment")

    async with ManySessionManager() as session:
        for attachment in attachments:
            tasks.append(download_one(session, attachment.sizes[-1].url))
        attachments_list.extend(await gather(*tasks))
    logger.debug("Fetched!")
    uploader = PhotoToAlbumUploader(api=scb.api.user_api)

    tasks = []
    for i in chunks(attachments_list, 5):
        tasks.append(uploader.upload(album_id=scb.grades.album_id, paths_like=i, group_id=scb.api.group_id))

    for i in await gather(*tasks):
        scb.storage["attachments"].extend(i)

    logger.debug("Uploaded.")

    await bp.api.messages.edit(
        peer_id=message.peer_id,
        message="✔ | Картинки загружены (%s шт.)!️" % len(attachments_list),
        message_id=sent
    )


async def download_one(session, url):
    resp = await session.request_content("GET", url)
    return resp


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
