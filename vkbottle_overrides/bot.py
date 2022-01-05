from utils.args_object import SCB
from vkbottle_overrides.tools.dev_tools.mini_types.bot import MessageMin
from .dispatch.rules import bot
from .framework.bot import BotBlueprint, Bot, SCBLabeler

Message = MessageMin
Blueprint = BotBlueprint
rules = bot
