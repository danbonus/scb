from enums.replaces import Replaces
from logger import logger


def process_replaces(current_day, subject):
    logger.debug("Replace found")
    logger.debug(subject.replace.type)
    logger.debug(Replaces.no_lesson)
    logger.debug(subject.replace.type == Replaces.no_lesson)
    if subject.replace.type == Replaces.no_lesson:
        logger.debug("No lesson: %s" % subject)
        current_day.pop(-1)
        text = "   ⌊ Урок отменён.\n"

    elif subject.replace.type == Replaces.room_changed:
        text = "   ⌊ Другой кабинет: %s.\n" % subject.replace.text
    elif subject.replace.type == Replaces.lesson_changed:
        text = "   ⌊ Другой урок: %s.\n" % subject.replace.text
    else:
        text = "   ⌊ Замещение: %s\n" % subject.replace.text
    return current_day, text
