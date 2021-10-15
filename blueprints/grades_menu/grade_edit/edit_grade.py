from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Grades edit"



@bp.on.message(rules.VBMLRule(["2", "Редактировать"]), state=GradesMenuStates.CMD_CHOICE)
async def edit_grade(message: Message, scb: SCB):
    pass
