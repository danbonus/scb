from random import randint
from string import Template

import datetime
from datetime import timedelta
from vkbottle import GroupTypes
from vkbottle import KeyboardButtonColor, Callback
from vkbottle.bot import Message

from keyboards.homework import HOMEWORK_KEYBOARD, USER_HOMEWORK_KEYBOARD
from logger import logger
from modules.homework import process_replaces
from utils.args_object import SCB
from vkbottle_overrides import Keyboard
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Homework"


@bp.on.private_message(payload={"cmd": "show_ids"})
@bp.on.private_message(text="Показать id")
async def homework(message: Message, scb: SCB):
    '''if "show_id" in scb.storage:
        if scb.storage["show_id"]:
            scb.storage["show_id"] = False
    else:
        scb.storage["show_id"] = True'''
    await get_homework(scb, show_ids=True)


@bp.on.private_message(payload={"cmd": "show_bells"})
@bp.on.private_message(text="Показать звонки")
async def homework(message: Message, scb: SCB):
    await get_homework(scb, show_bells=True)

@bp.on.message_event(payload={"cmd": "show_records_info"})
@bp.on.private_message(text="Показать инфу")
async def homework(message: Message, scb: SCB):
    if "show_records_info" in scb.storage:
        if scb.storage["show_records_info"]:
            scb.storage["show_records_info"] = False
    else:
        scb.storage["show_records_info"] = True
    await get_homework(scb)


@bp.on.private_message(text="дз <date>")
async def homework(message: Message, scb: SCB, date):
    await get_homework(scb, date=date)


@bp.on.private_message(text="Показать группы")
@bp.on.private_message(payload={"cmd": "show_groups"})
async def homework(event: GroupTypes.MessageEvent, scb):
    if "show_groups" in scb.storage:
        if scb.storage["show_groups"]:
            scb.storage["show_groups"] = False
        else:
            scb.storage["show_groups"] = True
    else:
        scb.storage["show_groups"] = True
    await get_homework(scb)


@bp.on.private_message(payload={"cmd": "show_homework"})
@bp.on.private_message(text=["дз", "lp", "рц", "hw", "pp", "wh", "зд"])
async def homework(message: Message, scb: SCB):
    if scb.user.is_writer:
        await message.answer("Техническое сообщение.", keyboard=HOMEWORK_KEYBOARD)
    elif scb.user.registered:
        await message.answer("Техническое сообщение.", keyboard=USER_HOMEWORK_KEYBOARD)
    await get_homework(scb)


async def get_homework(scb: SCB, date=None, send=True, show_bells=False, show_ids=False):
    show_groups = False if "show_groups" not in scb.storage else scb.storage["show_groups"]
    #display_id = False if "show_id" not in scb.storage else scb.storage["show_id"]
    display_id = show_ids
    show_records_info = False if "show_records_info" not in scb.storage else scb.storage["show_records_info"]
    this_day, tomorrow_day = scb.time.get_days_of_school()
    if date:
        this_day, tomorrow_day = scb.time.get_days_of_school(date)
        #print("New date: %s" % date)
        #print(this_day, tomorrow_day)
    attachments = []
    days_gen = scb.phrases.constants.days_gen
    days_acc = scb.phrases.constants.days_acc

    msg = Template(
        ("📚 | Домашнее задание для $grade с $day_from, $last_day_date: \n"
         "🕒 | Начало учебного дня в $last_day_first_bell, конец в $last_day_last_bell.\n\n"
         "$last_day_homework\n"
         "📚 | Домашнее задание для $grade на $day_to, $next_day_date: \n"
         "🕒 | Начало учебного дня в $next_day_first_bell, конец в $next_day_last_bell.\n\n"
         "$next_day_homework\n")
    )

    #    homework_list = [scb.homework.for_today(date), scb.homework.for_tomorrow(date)]

    homework_texts = []
    bells = []
    writers = set()
    processed_homework = []

    schedule = await scb.homework.nameitlater(date)
    logger.debug("Show groups: %s" % show_groups)
    attachments_number = 0
    subject_attachments = {}
    attachment_text = ""
    for day_homework in schedule:
        logger.debug([i.subject for i in day_homework])
        current_day = []
        homework_text = ""
        for i in day_homework:
            show_group_attachment = False
            subject_name = i.subject.nomn

            if i.subject.lang_group:
                if not show_groups:
                    logger.debug("I'm not supposed to show groups.")
                    if scb.user.lang_group != i.subject.lang_group:
                        logger.debug(
                            "Lang groups wrong! %s: %s" % (scb.user.lang_group, i.subject.lang_group)
                        )
                        continue
                    show_group_attachment = True
                else:
                    subject_name += i.subject.name
                    show_group_attachment = True

            if i.subject.exam_group:
                if not show_groups:
                    logger.debug("I'm not supposed to show groups.")
                    if scb.user.exam_group != i.subject.exam_group:
                        continue
                    show_group_attachment = True
                else:
                    subject_name += i.subject.name
                    show_group_attachment = True

            book = scb.utils.choice_book(i.homework.homework)
            element_in_brackets = i.room

            if display_id:
                element_in_brackets = i.homework.homework_id

            if show_bells:
                element_in_brackets = scb.grades.bells[i.bell].start + "-" + scb.grades.bells[i.bell].end

            current_day.append(i)
            if i.homework.attachments:
                if i.subject.exam_group or i.subject.lang_group:
                    if show_group_attachment:

                        attachments.extend(i.homework.attachments)
                        if i.subject.label in subject_attachments:
                            beu = subject_attachments[i.subject.label]
                        else:
                            beu = [str(attachments_number + i) for i in range(1, len(i.homework.attachments) + 1)]
                            subject_attachments[i.subject.label] = ', '.join(beu)
                            attachments_number += len(i.homework.attachments)
                        i.homework.homework += f'\n   ⌊ Картинки: №{", ".join(beu)}'

                else:
                    print('ХУЙЙЙЙЙЙЙЙЙЙ')
                    attachments.extend(i.homework.attachments)
                    if i.subject.label in subject_attachments:
                        beu = subject_attachments[i.subject.label]
                    else:
                        beu = [str(attachments_number + i) for i in range(1, len(i.homework.attachments) + 1)]
                        subject_attachments[i.subject.label] = ', '.join(beu)
                        attachments_number += len(i.homework.attachments)
                    i.homework.homework += f'\n   ⌊ Картинки: №{", ".join(beu)}'

            homework_text += scb.phrases.constants.homework_string.format(
                book, i.bell, element_in_brackets, subject_name, i.homework.homework
            )

            if i.replace:
                current_day, text = process_replaces(current_day, i)
                homework_text += text

            if i.homework.sender:
                if i.homework.sender > 0:
                    user = await scb.user.get(uid=i.homework.sender, case="ins")
                    writers.add(user.full_name)

        logger.debug(current_day[0].bell)
        logger.debug(current_day[-1].bell)
        logger.debug([i.subject for i in current_day])
        bells.append({
            "first_bell": scb.grades.bells[current_day[0].bell].start,
            "last_bell": scb.grades.bells[current_day[-1].bell].end
        })
        homework_texts.append(homework_text)

    msg = msg.substitute(
        grade=scb.user.grade,
        day_from=days_gen[str(this_day.weekday())].lower(),
        last_day_date=this_day.strftime("%d.%m.%Y"),
        last_day_first_bell=bells[0]["first_bell"],
        last_day_last_bell=bells[0]["last_bell"],
        last_day_homework=homework_texts[0],
        day_to=days_acc[str(tomorrow_day.weekday())].lower(),
        next_day_date=tomorrow_day.strftime("%d.%m.%Y"),
        next_day_first_bell=bells[1]["first_bell"],
        next_day_last_bell=bells[1]["last_bell"],
        next_day_homework=homework_texts[1]
    )

    if writers:
        msg += "📝 | Заполнено: %s." % ', '.join(writers)

    #attachments = list(dict.fromkeys(attachments))

    date_today = datetime.datetime.today()
    date_back = (date_today - timedelta(days=1)).strftime("%d.%m.%y")
    date_up = (date_today + timedelta(days=1)).strftime("%d.%m.%y")

    keyboard = Keyboard(inline=True)
    keyboard.add(Callback(date_back, {"date": date_back}), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Callback(date_today.strftime("%d.%m.%y"), {"date": date_today.strftime("%d.%m.%y")}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Callback(date_up, {"date": date_up}), color=KeyboardButtonColor.PRIMARY)
    keyboard = keyboard.get_json()
    sent = []
    sent_msgs = [msg]
    scb.storage["message_attachments"] = attachments
    if send:
        if not len(attachments) > 10:
            sent = [await bp.api.messages.send(user_id=scb.user.uid, message=msg, attachment=','.join(attachments), random_id=randint(-2e10, 2e10), keyboard=keyboard)]
            # await message.answer(message=msg, attachment=','.join(attachments))
        else:
            sent = [await bp.api.messages.send(user_id=scb.user.uid, message=msg, attachment=','.join(attachments[:10]), random_id=randint(-2e10, 2e10), keyboard=keyboard)]
            # await message.answer(message=msg, attachment=','.join(attachments[:10]))
            for i in scb.utils.chunks(attachments[10:], 10):
                sent.append(await bp.api.messages.send(user_id=scb.user.uid, message="Картинок было слишком много, держи остаток.", attachment=','.join(i), random_id=randint(-2e10, 2e10), keyboard=keyboard))
                sent_msgs.append("Картинок было слишком много, держи остаток.")
                # await message.answer(message="Картинок было слишком много, держи остаток.", attachment=','.join(i))
    
                # await message.answer(message="Картинок было слишком много, держи остаток.", attachment=','.join(i))
    if send:
        scb.storage["message_ids"] = sent
        await scb.requests.update(answered_message_id=sent[0])
    scb.storage["message_text"] = sent_msgs

    logger.debug("Attachments: %s" % attachments)
    # TODO доделать работу с картинок много
    return msg, attachments
