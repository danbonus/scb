from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
#from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD
from constants.states import GradesMenuStates
from vkbottle_overrides.bot import Message, rules
# from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD
from constants.states import GradesMenuStates
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Grades deletion"



@bp.on.private_message(rules.VBMLRule(["3", "Удалить"]), state=GradesMenuStates.CMD_CHOICE)
async def delete_grade(message: Message, scb: SCB):
    pass
