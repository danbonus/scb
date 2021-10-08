from vkbottle.tools.dev_tools.loop_wrapper import LoopWrapper
from logger import logger
from middlewares import middlewares
from rules import rules
from utils.api import bp, Api
from vkbottle.bot import Bot
from vkbottle_overrides.tools.dev_tools.utils import load_blueprints_from_package
from vkbottle import CtxStorage
from vkbottle_overrides.bot import SCBLabeler
import argparse


def init_bot(token):
    logger.info("SCB time! Starting.")
    lw = LoopWrapper(auto_reload=True)
    bot = Bot(token=token, loop_wrapper=lw)
    bot.labeler = SCBLabeler()
    bot.labeler.vbml_ignore_case = True  # беу == БЕУ == бЕу

    lw.on_startup.extend(
        [
            setup_api(bot),
            setup_rules(bot),
            setup_blueprints(bot),
            setup_middlewares(bot)
        ]
    )

    return bot


async def setup_blueprints(bot):
    """Это было чуток анально. В бутылке имеет вес положение хэндлера в списке, что, впрочем, логично.
    Благодаря этому можно построить простую логику: например, хэндлер первого обращения к боту должен быть
    самым первым, ибо иначе его может сожрать хэндлер регистрации и юзер не получит милую открытку с надписью
    <привет солнышко я сцб вижу ты тут в первый раз>"""

    bp.load(bot)
    handlers_count = 0
    blueprints = {}
    at_start = {
        "Registration": None
    }
    at_final = {
        "Anything": None
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


async def setup_middlewares(bot):
    middlewares_count = 0

    for i in middlewares:
        bot.labeler.message_view.register_middleware(i)
        middlewares_count += 1

    logger.info(f"Middlewares loaded: {middlewares_count}.")


async def setup_rules(bot):
    rules_count = 0

    for i in rules:
        logger.debug("Loading rule: %s" % i.__name__)  # имя рулза получено из имени файла
        bot.labeler.custom_rules[i.__name__] = i
        rules_count += 1

    logger.info(f"Rules loaded: {rules_count}")


async def setup_api(bot):
    storage = CtxStorage()
    storage.set("api", bot.api)
    storage.set("group_id", await Api(bot.api).get_group_id())
