from .dispatch.rules import bot
from .framework.bot import BotBlueprint, SCBLabeler
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from utils.args_object import SCB

Message = MessageMin
Blueprint = BotBlueprint
rules = bot
SCB = SCB
