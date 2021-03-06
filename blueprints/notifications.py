import random
from typing import Any

import time

from vkbottle.bot import Message
from vkbottle.modules import json

from keyboards.menu import MENU_KEYBOARD, WRITER_KEYBOARD, ADMIN_MENU_KEYBOARD
from logger import logger
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from rules.IsWriter import IsWriter
from constants.states import NotifyStates
from keyboards.misc import YN_KEYBOARD, BACK_TO_MENU
from keyboards.notifications import NOTIFY_TYPES_KEYBOARD
from vkbottle_overrides.dispatch.rules.bot import PayloadRule

bp = Blueprint()
bp.name = "Notifications"
bp.labeler.auto_rules.append(IsWriter())
#  phrases.load(Menu)


@bp.on.private_message(payload={"cmd": "notify"})
@bp.on.private_message(text="Оповестить")
async def ask_for_text(message: Message, scb: SCB):
    await message.answer("Выбери тип пользователей для рассылки оповещения.", keyboard=NOTIFY_TYPES_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, NotifyStates.GET_USERS)


@bp.on.private_message(state=NotifyStates.GET_USERS)
async def ask_for_text(message: Message, scb: SCB):
    payload = json.loads(message.payload)
    key = list(payload.keys())[0]
    value = list(payload.values())[0]

    if key == 'is_writer':
        users = await scb.many_users.get_writers()
    else:
        users = await scb.many_users.get_many(key, value)
    scb.storage["users"] = users
    await message.answer(message="Теперь напиши текст оповещения.", keyboard=BACK_TO_MENU)
    await bp.state_dispenser.set(message.peer_id, NotifyStates.GET_TEXT)


@bp.on.private_message(state=NotifyStates.GET_TEXT)
async def confirm(message: Message, scb: SCB):
    scb.storage["notify_text"] = message.text
    users = scb.storage["users"]

    await message.answer(
        "Текст оповещения: %s. \n\nЮзеры: \n%s\n\nРассылаю?" % (
            message.text,
            '\n'.join(f'{index + 1}. [id{i.uid}|{i.last_name} {i.first_name}]' for index, i in enumerate(users))
        ),
        keyboard=YN_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, NotifyStates.CONFIRM)


@bp.on.private_message(payload={"action": True}, state=NotifyStates.CONFIRM)
async def send(message: Message, scb: SCB):
    users = scb.storage["users"]
    sent = await message.answer("Рассылаю...", keyboard=BACK_TO_MENU)
    scb.storage["animated_message_text"] = "Рассылаю..."
    logger.debug("New attachment")

    await notify(users, scb.user, sent, scb.storage["notify_text"], scb)

    await bp.state_dispenser.delete(message.peer_id)


async def notify(users, writer, message_id, notify_text, scb):
    for i in users:
        if i.uid == writer.uid:
            continue
        try:
            await bp.api.messages.send(
                peer_id=i.uid,
                message=f"🔔 | Оповещение, отправил [id{writer.uid}|{writer.full_name}]: \n\n {notify_text}",
                random_id=random.randint(-2e10, 2e10)
            )
            scb.storage["animated_message_text"] = scb.storage[
                                                       "animated_message_text"] + f"\n✔ | [id{i.uid}|{i.last_name} {i.first_name}]"
            time.sleep(0.3)
        except:
            scb.storage["animated_message_text"] = scb.storage["animated_message_text"] + f"\n❌ | [id{i.uid}|{i.last_name} {i.first_name}]"

        await bp.api.messages.edit(
            peer_id=writer.uid,
            message=scb.storage["animated_message_text"],
            message_id=message_id
        )


@bp.on.private_message(payload={"action": False}, state=NotifyStates.CONFIRM)
async def deny(message: Message, scb: SCB):
    await message.answer("да какого хуя? \nБлядь, да мне похуй на тебя, блядь, слушай. Какая у тебя там тачка, блядь, квартиры, срачки, там блядь, яхты, всё — мне похуй там. Хоть «Бентли», хоть, блядь, нахуй, «Майбах», хоть «Роллс-Ройс», хоть «Бугатти», блядь, хоть стометровая яхта — мне на это насрать, понимаешь? Сколько ты там, кого ебёшь, каких баб, каких, значит, вот этих самок, шикарных или атласных, блядь, в космос ли ты летишь — мне на это насрать, понимаешь? Я, блядь, в своем познании настолько преисполнился, что я как будто бы уже сто триллионов миллиардов лет, блядь, проживаю на триллионах и триллионах таких же планет, понимаешь? Как эта Земля. Мне уже этот мир абсолютно понятен, и я здесь ищу только одного, блядь: покоя, умиротворения и вот этой гармонии от слияния с бесконечно вечным, от созерцания этого великого фрактального подобия и от вот этого вот замечательного всеединства существа бесконечно вечного — куда ни посмотри: хоть в глубь — бесконечно малое, хоть ввысь — бесконечно большое, понимаешь? А ты мне опять со своими, там, это. Иди, суетись дальше, твое распределение — это твой путь и твой горизонт познания, ощущения и твоей природы. И он несоизмеримо мелок по сравнению с моим, понимаешь? Я как будто уже глубокий старец бессмертный или, там, уже почти бессмертный, который на этой планете от её самого зарождения, еще когда только Солнце только-только сформировалось как звезда и вот это газопылевое облако, вот, после взрыва Солнца, когда оно вспыхнуло, как звезда, начало формировать коацерваты-планеты, понимаешь? Я на этой Земле уже как будто почти пять миллиардов лет, блядь, живу и знаю её уже вдоль и поперек, этот весь мир, а ты мне, там, какие-то это. Мне похуй на твои тачки, на твои, блядь, нахуй, яхты, на твои квартиры, там, на твоё благо, понимаешь? Я был на этой планете, так сказать, или бесконечном множестве, и круче Цезаря, и круче Гитлера, блядь, и круче всех великих, понимаешь, был? А где-то был конченым говном, ещё хуже, чем здесь. Потому что я множество этих состояний чувствую. Где-то я был больше подобен растению, где-то был больше подобен птице, там, червю, где-то просто был сгусток камня. Это все есть душа, понимаешь? Она вот имеет грани подобия совершенно многообразные, бесконечное множество. Но тебе этого не понять, поэтому ты езжай себе, блядь. Мы в этом мире как бы живём разными ощущениями, разными стремлениями. Соответственно, разное наше и место, разное наше распределение. Тебе я желаю, все самые крутые тачки чтобы были у тебя, и все самые лучшие самки, чтобы раздвигали перед тобой ноги там, все свои щели нашиворот-навыворот, блядь, перед тобой, как ковёр, это самое, раскрывали и растлевали, растлали. И ты их чтобы ебал, до посинения, до красна, до солнца закатного. Чтоб на лучших яхтах, на самолётах летал и кончал прямо с иллюминатора и всё, что только может в голову прийти и не прийти. Если мало идей – обращайся ко мне, я тебе на каждую твою идею еще сотни триллионов подскажу как, что делать. Ну а я всё, я иду, как глубокий старец, узривший вечное, прикоснувшийся к божественному, сам стал богоподобен и устремлен в это бесконечное, который в умиротворении, покое, гармонии, благодати, в этом сокровенном блаженстве пребывает, вовлечённый во всё и во вся, понимаешь? Вот и всё. В этом наша разница. Так что, я иду любоваться мирозданием, а ты идёшь какой-то преисполняться в гранях каких-то. Вот и вся разница, понимаешь? Ты не зришь это вечное бесконечное, оно тебе не нужно. Но зато ты, так сказать, более активен, как вот этот дятел долбящий или муравей, который вот очень активен в своей стезе, вот и всё. Поэтому давай, наши пути здесь, так сказать, имеют, конечно, грани подобия, потому что всё едино, но ты меня… Я-то тебя прекрасно понимаю, а вот ты — вряд ли, потому что, как бы, я, ты и, как бы, я тебя в себе содержу — всю твою природу, она составляет одну маленькую, там, песчиночку от того, что есть во мне, понимаешь? Вот и всё. Поэтому давай ступай, езжай, а я пошел наслаждаться, нахуй, блядь, прекрасным осенним закатом, блядь, на берегу тёплой южной реки. Всё, пиздуй-бороздуй и я попиздил нахуй.", keyboard=BACK_TO_MENU)
    await bp.state_dispenser.delete(message.peer_id)
