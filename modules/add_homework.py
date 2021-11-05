from utils.api_test import Pagination
from constants.keyboards import iteration_keyboard, subjects_keyboard, RETURN_KEYBOARD, CREATE_SUBJECT_KEYBOARD
from utils.args_object import SCB
from logger import logger


async def get_subjects(scb: SCB, payload, date=None):
    grade_subjects = scb.subjects.grades_subjects
    priority_subjects = []
    scb.storage["deadline"] = None
    scb.storage["attachments"] = []
    already_filled = [i async for i in scb.homework.get_filled_for_today()]
    #logger.debug(already_filled)

    grade_subjects = list(filter(lambda i: not i.lang_group, grade_subjects))
    logger.debug(grade_subjects)
    grade_subjects = list(filter(lambda i: not i.ege_group, grade_subjects))
    logger.debug(grade_subjects)
    '''for index, i in enumerate(grade_subjects):  # удаление предметов с группами из клавиатуры
        logger.debug(i)
        logger.debug(i.lang_group)
        if i.lang_group or i.ege_group:
            logger.debug("Popping")
            grade_subjects.remove(i)'''

    for schedule in (await scb.homework.nameitlater()):
        for i in schedule:
            logger.debug(i.subject)
            logger.debug(i.subject.lang_group)

            if i.subject in priority_subjects:  # спаренные уроки
                continue

            if i.subject not in already_filled:
                if not i.subject.lang_group and not i.subject.ege_group:
                    priority_subjects.append(i.subject)
                else:
                    if scb.subjects[i.subject.label[:-1]] not in priority_subjects:
                        priority_subjects.append(scb.subjects[i.subject.label[:-1]])
                #if i.subject in grade_subjects:
                #    grade_subjects.pop(grade_subjects.index(i.subject))

    logger.debug(priority_subjects)
    grade_subjects = list(filter(lambda i: i not in priority_subjects, grade_subjects))
    logger.debug(grade_subjects)
    grade_subjects[:0] = priority_subjects
    logger.debug(grade_subjects)
    pagination = Pagination(grade_subjects, 6, payload, inline=False)
    page_subjects, page_keyboard = pagination.get()

    subjects_plain, keyboard = subjects_keyboard([subject for subject in page_subjects])

    return keyboard + page_keyboard
