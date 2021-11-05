import enum
from vkbottle_types import BaseStateGroup


@enum.unique
class RegistrationStates(BaseStateGroup):
    REGISTRATION_START = 0
    LANGUAGE_STATE = 1
    GRADE_CHECK = 2
    BROADCAST_STATE = 3
    FINAL_STATE = 4


@enum.unique
class BroadcastStates(BaseStateGroup):
    ENABLE_BROADCAST = 5
    BROADCAST_TYPE = 6
    BROADCAST_TIME = 7


@enum.unique
class GradesMenuStates(BaseStateGroup):
    CMD_CHOICE = 8


@enum.unique
class GradeCreationStates(BaseStateGroup):
    CMD_CHOICE = 9
    LABEL = 10
    ALBUM_id = 11
    FIRST_BELL = 12
    BELLS = 13
    SUBJECTS = 14
    SCHEDULE = 15
    END = 16

@enum.unique
class SubjectCreationStates(BaseStateGroup):
    SUBJECT_LANG = 17
    SUBJECT_LABEL = 18
    SUBJECT_NAME = 19
    SUBJECT_SHORTS = 20
    SUBJECT_EMOJI = 21


@enum.unique
class HomeworkCreationStates(BaseStateGroup):
    GET_SUBJECT = 22
    HOMEWORK_TEXT = 23
    OPTIONAL = 24
    FILLED = 25


class EmulationStates(BaseStateGroup):
    EMULATION_DAY = 26
    EMULATION_INPUT = 27


GradeCreationStatesList = list(map(int, GradeCreationStates))
