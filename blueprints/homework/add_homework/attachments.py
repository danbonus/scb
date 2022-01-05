from asyncio import gather

from vkbottle import PhotoToAlbumUploader
from vkbottle.bot import Message
from vkbottle.http import ManySessionManager

from constants.states import HomeworkCreationStates
from logger import logger
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from PIL import Image, ImageFont, ImageDraw
import random
import io

bp = Blueprint()
bp.name = "HW ADD: attachments"


@bp.on.private_message(
    func=lambda message: len(message.get_photo_attachments()) > 0 or len(message.get_doc_attachments()) > 0,
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
    last_day, next_day = scb.time.get_days_of_school()
    print(scb.storage['readable_subject_name'])
    async with ManySessionManager() as session:
        for attachment in attachments:
            tasks.append(
                process_one(
                    session,
                    attachment.sizes[-1].url,
                    f"{next_day.strftime('%d.%m.%Y')} {scb.storage['readable_subject_name']}."
                )
            )
        attachments_list.extend(await gather(*tasks))

    logger.debug("Fetched!")
    uploader = PhotoToAlbumUploader(api=scb.api.user_api)

    tasks = []
    for i in scb.utils.chunks(attachments_list, 5):
        tasks.append(uploader.upload(album_id=scb.grades.album_id, paths_like=i, group_id=scb.api.group_id))

    for i in await gather(*tasks):
        scb.storage["attachments"].extend(i)

    logger.debug("Uploaded.")

    await bp.api.messages.edit(
        peer_id=message.peer_id,
        message="✔ | Картинки загружены (%s шт.)!️" % len(attachments_list),
        message_id=sent
    )


async def process_one(session, url, caption):
    resp = await session.request_content("GET", url)

    edited_photo = await edit_photo(resp, caption)

    return edited_photo


async def edit_photo(image, text):
    print(type(image))
    img = Image.open(io.BytesIO(image))
    img.load()
    fontsize = 1
    img_fraction = 0.05

    logger.info("Size of the Image: ")
    logger.info(img.size)

    img_w, img_h = img.size
    rectangle_size = int(img_h / 100 * 7)
    logger.info("Rectangle size" + str(rectangle_size))

    bg = Image.new('RGB', (img_w, img_h + rectangle_size))
    bg.paste(img, (0, rectangle_size))

    font = ImageFont.truetype("bahnschrift.ttf", fontsize)

    while font.getsize(text)[1] < img_fraction * img_h:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("bahnschrift.ttf", fontsize)

    font = ImageFont.truetype("bahnschrift.ttf", fontsize)

    print("Final size: " + str(fontsize))

    draw = ImageDraw.Draw(bg)
    draw.text((10, rectangle_size / 7), text, font=font, fill=(255, 255, 255, 128))

    #path = "/home/pi/scb/photos/photo_%s.jpg" % int(random.randint(0, 1590296287))
    #bg.save(path, "JPEG")

    with io.BytesIO() as output:
        bg.save(output, "JPEG")
        contents = output.getvalue()

    return contents