import enum
from vkbottle_types import BaseStateGroup


@enum.unique
class RegistrationStates(BaseStateGroup):
    GRADE_STATE = 0
    GRADE_CHECK = 1
    BROADCAST_STATE = 2
    BROADCAST_TYPE = 3
    BROADCAST_TIME = 4
    FINAL_STATE = 5


@enum.unique
class GradesMenuStates(BaseStateGroup):
    CMD_CHOICE = 6


@enum.unique
class GradeCreationStates(BaseStateGroup):
    LABEL = 7
    ALBUM_id = 8
    FIRST_BELL = 9
    BELLS = 10
    SUBJECT_LANG = 11
    SUBJECT_LABEL = 12
    SUBJECT_NAME = 13
    SUBJECT_SHORTS = 14
    SUBJECT_EMOJI = 15

    SCHEDULE = 16
    END = 17


GradeCreationStatesList = list(map(int, GradeCreationStates))
