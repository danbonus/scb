from keyboards.subjects import subjects_iteration, subjects_to_delete_iteration
from logger import logger
from utils.api_test import Pagination
from utils.args_object import SCB


async def get_subjects(scb: SCB, payload, date=None, skip_filled=True, skip_foreign_groups=True):
    grade_subjects = scb.subjects.grades_subjects
    priority_subjects = []
    scb.storage["deadline"] = None
    scb.storage["attachments"] = []
    already_filled = [i async for i in scb.homework.get_filled()]
    #logger.debug(already_filled)

    if skip_foreign_groups:
        grade_subjects = list(filter(lambda i: not i.lang_group, grade_subjects))
        logger.debug(grade_subjects)
        grade_subjects = list(filter(lambda i: not i.exam_group, grade_subjects))
        logger.debug(grade_subjects)
    '''else:
        lang_subjects = list(filter(lambda i: i.lang_group, grade_subjects))
        exam_subjects = list(filter(lambda i: i.exam_group, grade_subjects))
        for i in [lang_subjects, exam_subjects]:
            for _ in i:
                grade_subjects = list(filter(lambda a: a.label != _.label[:-1], grade_subjects))'''

    '''for index, i in enumerate(grade_subjects):  # удаление предметов с группами из клавиатуры
        logger.debug(i)
        logger.debug(i.lang_group)
        if i.lang_group or i.exam_group:
            logger.debug("Popping")
            grade_subjects.remove(i)'''

    for schedule in (await scb.homework.nameitlater()):
        if skip_filled:
            schedule = list(filter(lambda i: i.subject not in already_filled, schedule))
        for i in schedule:
            logger.debug(i.subject)
            logger.debug(i.subject.lang_group)

            if i.subject in priority_subjects:  # спаренные уроки
                continue

            if not i.subject.lang_group and not i.subject.exam_group:
                priority_subjects.append(i.subject)
            else:
                if scb.subjects[i.subject.label[:-1]] not in priority_subjects:
                    if skip_foreign_groups:
                        logger.debug('skipping foreign groups')
                        priority_subjects.append(scb.subjects[i.subject.label[:-1]])
                    else:
                        logger.debug('not skipping foreign groups')
                        priority_subjects.append(scb.subjects[i.subject.label])

                #if i.subject in grade_subjects:
                #    grade_subjects.pop(grade_subjects.index(i.subject))

    logger.debug(priority_subjects)
    grade_subjects = list(filter(lambda i: i not in priority_subjects, grade_subjects))
    logger.debug(grade_subjects)
    grade_subjects[:0] = priority_subjects
    logger.debug(grade_subjects)
    pagination = Pagination(grade_subjects, 10, payload, inline=False)
    page_subjects, page_keyboard = pagination.get()
    if skip_filled:
        subjects_plain, keyboard = subjects_iteration([subject for subject in page_subjects], row=2)
    else:
        #subjects_plain, keyboard = subjects_to_delete_iteration([subject for subject in page_subjects])
        subjects_plain, keyboard = subjects_iteration([subject for subject in page_subjects], row=2)


    return keyboard + page_keyboard
