from rules.IsAdmin import IsAdmin
from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Broadcast adm"
bp.labeler.auto_rules.append(IsAdmin())
