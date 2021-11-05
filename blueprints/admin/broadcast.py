from vkbottle_overrides.bot import Blueprint
from vkbottle.bot import Message
from utils.args_object import SCB
from constants.states import BroadcastStates
from constants.keyboards import RETURN_KEYBOARD, BROADCAST_TYPE_KEYBOARD, TIME_SINCE_KEYBOARD, TIME_FIXED_KEYBOARD, MENU_KEYBOARD, YN_KEYBOARD
from datetime import datetime
import json
from vkbottle import GroupEventType, GroupTypes
from rules.IsAdmin import IsAdmin
from logger import logger
from modules.add_homework import get_subjects
bp = Blueprint()
bp.name = "Broadcast adm"
bp.labeler.auto_rules.append(IsAdmin())
