from constants.states import GradesMenuStates
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
from vkbottle_overrides.bot import Message, rules

bp = Blueprint()
bp.name = "Grades list"



@bp.on.private_message(rules.VBMLRule(["4", "Список классов"]), state=GradesMenuStates.CMD_CHOICE)
async def grades_list(message: Message, scb: SCB):
    pass