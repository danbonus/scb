import enum

from vkbottle_types import BaseStateGroup


@enum.unique
class RegistrationStates(BaseStateGroup):
    REGISTRATION_START = 0
    LANGUAGE_STATE = 1
    GRADE_CHECK = 2
    GET_LANG_GROUP = 3
    GET_EXAM_GROUP = 4
    BROADCAST_STATE = 5
    FINAL_STATE = 6


@enum.unique
class BroadcastStates(BaseStateGroup):
    ENABLE_BROADCAST = 7
    BROADCAST_TYPE = 8
    BROADCAST_TIME = 9


@enum.unique
class GradesMenuStates(BaseStateGroup):
    CMD_CHOICE = 10


@enum.unique
class GradeCreationStates(BaseStateGroup):
    CMD_CHOICE = 11
    LABEL = 12
    ALBUM_id = 13
    FIRST_BELL = 14
    BELLS = 15
    SUBJECTS = 16
    SCHEDULE = 17
    END = 18


@enum.unique
class SubjectCreationStates(BaseStateGroup):
    SUBJECT_LANG = 19
    SUBJECT_LABEL = 20
    SUBJECT_NAME = 21
    SUBJECT_SHORTS = 22
    SUBJECT_EMOJI = 23


@enum.unique
class HomeworkCreationStates(BaseStateGroup):
    GET_SUBJECT = 24
    HOMEWORK_TEXT = 25
    OPTIONAL = 26
    FILLED = 27


class EmulationStates(BaseStateGroup):
    EMULATION_DAY = 28
    EMULATION_INPUT = 29


class ReplaceCreationStates(BaseStateGroup):
    GET_DAY = 31
    GET_CUSTOM_DAY = 32
    GET_LESSON = 33
    GET_TYPE = 34
    GET_TEXT = 35


class NotifyStates(BaseStateGroup):
    GET_USERS = 36
    GET_TEXT = 37
    CONFIRM = 38


class HomeworkDeletionStates(BaseStateGroup):
    GET_SUBJECT = 39
    CONFIRM = 40


GradeCreationStatesList = list(map(int, GradeCreationStates))
