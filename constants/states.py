import enum
from vkbottle_types import BaseStateGroup


@enum.unique
class RegistrationStates(BaseStateGroup):
    REGISTRATION_START = 0
    LANGUAGE_STATE = 1
    GRADE_CHECK = 2
    BROADCAST_STATE = 3
    BROADCAST_TYPE = 4
    BROADCAST_TIME = 5
    FINAL_STATE = 6


@enum.unique
class GradesMenuStates(BaseStateGroup):
    CMD_CHOICE = 7


@enum.unique
class GradeCreationStates(BaseStateGroup):
    CMD_CHOICE = 7
    LABEL = 8
    ALBUM_id = 9
    FIRST_BELL = 10
    BELLS = 11
    SUBJECTS = 12
    SCHEDULE = 13
    END = 14

@enum.unique
class SubjectCreationStates(BaseStateGroup):
    SUBJECT_LANG = 15
    SUBJECT_LABEL = 16
    SUBJECT_NAME = 17
    SUBJECT_SHORTS = 18
    SUBJECT_EMOJI = 19


@enum.unique
class HomeworkCreationStates(BaseStateGroup):
    GET_SUBJECT = 20
    HOMEWORK_TEXT = 21
    HOMEWORK_ATTACHMENTS = 22


GradeCreationStatesList = list(map(int, GradeCreationStates))
