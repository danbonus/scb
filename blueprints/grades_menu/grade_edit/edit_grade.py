from constants.states import GradesMenuStates
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Grades edit"



@bp.on.private_message(rules.VBMLRule(["2", "Редактировать"]), state=GradesMenuStates.CMD_CHOICE)
async def edit_grade(message: Message, scb: SCB):
    pass
