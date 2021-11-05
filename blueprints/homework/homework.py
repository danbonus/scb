from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
import datetime
from string import Template
from random import randint
from rules.IsWriter import IsWriter
import json
from vkbottle import GroupEventType, GroupTypes
from vkbottle import KeyboardButtonColor, Text, EMPTY_KEYBOARD, Callback
from vkbottle_overrides import Keyboard
from constants.keyboards import RETURN_KEYBOARD
from datetime import timedelta


bp = Blueprint()
bp.name = "Homework"


@bp.on.message(text="дз -id")
async def homework(message: Message, scb: SCB):
    scb.storage["show_id"] = True
    await get_homework(scb)


@bp.on.message_event(payload={"cmd": "show_id"})
async def homework(message: Message, scb: SCB):
    scb.storage["show_id"] = True
    await get_homework(scb)


@bp.on.message(text="дз <date>")
async def homework(message: Message, scb: SCB, date):
    await get_homework(scb, date=date)


@bp.on.message(text="Показать группы")
@bp.on.message_event(payload={"cmd": "show_groups"})
async def homework(event: GroupTypes.MessageEvent, scb):
    scb.storage["show_groups"] = True
    await get_homework(scb)


@bp.on.message(text=["дз", "lp", "рц", "hw"])
async def homework(message: Message, scb: SCB):
    await get_homework(scb)


async def get_homework(scb: SCB = None, date=None, send=True):
    show_groups = False if "show_groups" not in scb.storage else scb.storage["show_groups"]
    display_id = False if "show_id" not in scb.storage else scb.storage["show_id"]
    this_day, tomorrow_day = scb.time.get_days_of_school()
    if date:
        #this_day = datetime.datetime.strptime(date, "%d.%m.%Y")
        #tomorrow_day = this_day + datetime.timedelta(days=1)
        this_day, tomorrow_day = scb.time.get_days_of_school(date)
        print("New date: %s" % date)
        print(this_day, tomorrow_day)
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

    for day_homework in await scb.homework.nameitlater(date):
        homework_text = ""
        for i in day_homework:
            subject_name = i.subject.nomn

            if i.subject.lang_group:
                if not show_groups:
                    if scb.user.lang_group != i.subject.lang_group:
                        continue
                else:
                    subject_name += i.subject.name

            if i.subject.ege_group:
                if not show_groups:
                    if scb.user.ege_group != i.subject.ege_group:
                        continue
                else:
                    subject_name += i.subject.name

            book = scb.utils.choice_book(i.homework.homework)
            element_in_brackets = i.room
            if display_id:
                element_in_brackets = i.homework.homework_id
            homework_text += scb.phrases.constants.homework_string.format(
                book, i.bell, element_in_brackets, subject_name, i.homework.homework
            )
            attachments.extend(i.homework.attachments)
            if i.homework.sender:
                user = await scb.user.get(uid=i.homework.sender, case="ins")
                writers.add(user.full_name)

        bells.append({
            "first_bell": scb.grades.bells[day_homework[0].bell].start,
            "last_bell": scb.grades.bells[day_homework[-1].bell].end
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

    attachments = list(dict.fromkeys(attachments))

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
    scb.storage["message_text"] = sent_msgs
    # TODO доделать работу с картинок много
