from vkbottle_overrides.bot import Blueprint

#from constants.keyboards import FIRST_BELL, RETURN_KEYBOARD, PASS_KEYBOARD

bp = Blueprint()
bp.name = "Reload Modules"

from logger import logger
from vkbottle_overrides.tools.dev_tools.utils import load_blueprints_from_package


async def setup_blueprints(bot):
    """Это было чуток анально. В бутылке имеет вес положение хэндлера в списке, что, впрочем, логично.
    Благодаря этому можно построить простую логику: например, хэндлер первого обращения к боту должен быть
    самым первым, ибо иначе его может сожрать хэндлер регистрации и юзер не получит милую открытку с надписью
    <привет солнышко я сцб вижу ты тут в первый раз>"""

    bp.load(bot)
    handlers_count = 0
    blueprints = {}
    at_start = {
        "Registration": None,
        "Back Handler": None
    }
    at_final = {
        "Menu": None
    }

    for i in load_blueprints_from_package("blueprints"):
        if i.name in at_final:
            at_final[i.name] = i

        elif i.name in at_start:
            at_start[i.name] = i

        else:
            blueprints[i.name] = i

        handlers_count += 1

    for i in at_start:  # получение объекта blueprint через ключ имени этого блюпринта
        at_start[i].load(bot)
        logger.debug("Loading START handler: %s" % i)

    for i in blueprints:
        blueprints[i].load(bot)
        logger.debug("Loading handler: %s" % i)

    for i in at_final:
        at_final[i].load(bot)
        logger.debug("Loading FINAL handler: %s" % i)

    logger.info(f"Handlers loaded: {handlers_count}.")
