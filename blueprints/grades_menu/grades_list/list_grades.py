from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.keyboards import GRADES_KEYBOARD, PASS_KEYBOARD
from constants.states import GradesMenuStates, GradeCreationStates
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Grades list"



@bp.on.message(rules.VBMLRule(["4", "Список классов"]), state=GradesMenuStates.CMD_CHOICE)
async def grades_list(message: Message, scb: SCB):
    pass