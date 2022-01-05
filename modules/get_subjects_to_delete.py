from keyboards.subjects import subjects_iteration, subjects_to_delete_iteration
from logger import logger
from utils.api_test import Pagination
from utils.args_object import SCB


async def get_subjects_to_delete(scb: SCB, payload):
    #grade_subjects = scb.subjects.grades_subjects
    priority_subjects = []
    scb.storage["deadline"] = None
    scb.storage["attachments"] = []

    '''grade_subjects = list(filter(lambda i: not i.lang_group, grade_subjects))
    logger.debug(grade_subjects)
    grade_subjects = list(filter(lambda i: not i.exam_group, grade_subjects))
    logger.debug(grade_subjects)

    for schedule in (await scb.homework.nameitlater()):
        for i in schedule:
            logger.debug(i.subject)
            logger.debug(i.subject.lang_group)

            if i.subject in priority_subjects:  # спаренные уроки
                continue

            if not i.subject.lang_group and not i.subject.exam_group:
                priority_subjects.append(i)
            else:
                if scb.subjects[i.subject.label[:-1]] not in priority_subjects:
                    priority_subjects.append(i)

    logger.debug(priority_subjects)
    grade_subjects = list(filter(lambda i: i not in priority_subjects, grade_subjects))
    logger.debug(grade_subjects)
    grade_subjects[:0] = priority_subjects
    logger.debug(grade_subjects)'''
    if 'offset' not in payload:
        offset = 0
    else:
        offset = payload['offset']
    print('offset: %s' % offset)
    print(payload)
    count, lessons = await scb.homework.get_records(scb.subjects, offset=offset)
    print(', '.join([str(i.homework_id) for i in lessons]))
    pagination = Pagination(lessons, 8, payload, inline=False, count=count, pagination_type="removing", offset=offset)
    page_subjects, page_keyboard = pagination.get()
    print(page_subjects)
    subjects_plain, keyboard = subjects_to_delete_iteration([subject for subject in page_subjects], row=1)
    return keyboard + page_keyboard
