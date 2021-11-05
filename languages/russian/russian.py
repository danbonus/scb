from string import Template
from . import registration, grade_creation, broadcast, menu, subjects



class Constants:
    days = {
        "0": "Понедельник",
        "1": "Вторник",
        "2": "Среда",
        "3": "Четверг",
        "4": "Пятница",
        "5": "Суббота",
        "6": "Воскресенье"
    }

    days_gen = {
        "0": "Понедельника",
        "1": "Вторника",
        "2": "Среды",
        "3": "Четверга",
        "4": "Пятницы",
        "5": "Субботы",
        "6": "Воскресенья"
    }

    days_acc = {
        "0": "Понедельник",
        "1": "Вторник",
        "2": "Среду",
        "3": "Четверг",
        "4": "Пятницу",
        "5": "Субботу",
        "6": "Воскресенье"
    }

    homework_string = "{0} | {1}. [{2}] {3}: {4}\n"


class DefaultLanguage:
    __name__ = "russian"
    __greetings__ = {
        "greeting": "Ты можешь узнать список команд, введя <<команды>> без кавычек.",
        "morning": "🌅 | Доброе утро, %s!\n",
        "afternoon": "⛰️ | Добрый день, %s!\n",
        "evening": "🌇 | Добрый вечер, %s!\n",
        "night": "🌃 | Здравствуй, %s!\n"
    }

    registration = registration.Registration
    grade_creation = grade_creation.Grades
    broadcast = broadcast.Broadcast
    menu = menu.Menu
    constants = Constants
    subjects = subjects.DefaultSubjects
