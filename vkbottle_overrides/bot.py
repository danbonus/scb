from .dispatch.rules import bot
from .framework.bot import BotBlueprint, SCBLabeler
from vkbottle_overrides.tools.dev_tools.mini_types.bot import MessageMin
from utils.args_object import SCB
from .framework.bot import Bot

Message = MessageMin
Blueprint = BotBlueprint
rules = bot
SCB = SCB
