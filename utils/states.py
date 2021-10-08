from vkbottle_types import BaseStateGroup


class RegistrationStates(BaseStateGroup):
    GRADE_STATE = 0
    GRADE_CHECK = 1
    BROADCAST_STATE = 2
    BROADCAST_TYPE = 3
    BROADCAST_TIME = 4
    FINAL_STATE = 5
