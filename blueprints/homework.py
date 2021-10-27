from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import BotLabeler, Message
from repositories.user import UserRepository
from constants import MENU_KEYBOARD
from utils.args_object import SCB


bp = Blueprint()
bp.name = "Homework"
#  phrases.load(Menu)


@bp.on.message(text="ДЗ")
async def homework(message: Message, scb: SCB):
    user = scb.user
    this_day, tomorrow_day = scb.time.check_for_weekday()

    grade_subjects = scb.subjects.grades_subjects
    msg = f" 📚 | Домашнее задание для {scb.user.grade} с %s: \n\n" % scb.phrases.constants.days_gen[str(this_day.weekday())].lower()

    today_subjects = {}
    async for i in await scb.homework.for_today:
        print("iterating")
        book = choice_book(i.homework.homework)
        msg += f"{book} | {i.bell}. [{i.room}] {i.subject.nomn}: {i.homework.homework}\n"

    msg += f"\n📚 | Домашнее задание для {scb.user.grade} на %s: \n\n" % scb.phrases.constants.days_acc[str(tomorrow_day.weekday())].lower()

    async for i in await scb.homework.for_tomorrow:
        print("iterating")
        book = choice_book(i.homework.homework)
        msg += f"{book} | {i.bell}. [{i.room}] {i.subject.nomn}: {i.homework.homework}\n"

    return msg


def choice_book(hw):
    book = "📘"
    books_names = {
        "ничего.": "📗",
        "ещё неизвестно.": "📔",
        "неизвестно.": "📕"
    }

    if hw in list(books_names.keys()):
        book = books_names[hw]

    return book