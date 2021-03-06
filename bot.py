from logger import logger
from middlewares import middlewares
from middlewares.EventAnswerMiddleware import EventAnswerMiddleware
from middlewares.OutdatedEventMiddleware import OutdatedEventMiddleware
from modules.change_title import change_title
from rules import rules
from utils.api import Api
from utils.broadcast import broadcast
from vkbottle_overrides.bot import Bot
from vkbottle_overrides.bot import SCBLabeler
from vkbottle_overrides.dispatch.dispenser import BuiltinStateDispenser
from vkbottle_overrides.tools.dev_tools.loop_wrapper import LoopWrapper
from vkbottle_overrides.tools.dev_tools.utils import load_blueprints_from_package
import aioschedule as schedule
from modules.writers_reminder import remind_writers


def init_bot(token) -> Bot:
    logger.success("SCB time! Starting.")
    lw = LoopWrapper()
    bot = Bot(token=token, loop_wrapper=lw)
    bot.state_dispenser = BuiltinStateDispenser()
    bot.labeler = SCBLabeler()
    bot.labeler.vbml_ignore_case = True  # беу == БЕУ == бЕу

    lw.on_startup.extend(
        [
            setup_api(bot),
            setup_rules(bot),
            setup_blueprints(bot),
            setup_middlewares(bot),
        ]
    )
    #lw.create_timer(broadcast, seconds=40)
    lw.create_interval(change_title, minutes=10, api=Api)
    #lw.create_timer(remind_writers, schedule=schedule, seconds=1)
    lw.create_interval(schedule.run_pending, seconds=1)
    #lw.create_timer(schedule.run_pending, seconds=1)
    return bot


async def beu():
    print("сработало")


async def setup_blueprints(bot):
    """Это было чуток анально. В бутылке имеет вес положение хэндлера в списке, что, впрочем, логично.
    Благодаря этому можно построить простую логику: например, хэндлер первого обращения к боту должен быть
    самым первым, ибо иначе его может сожрать хэндлер регистрации и юзер не получит милую открытку с надписью
    <привет солнышко я сцб вижу ты тут в первый раз>"""

    handlers_count = 0
    blueprints = {}
    at_start = {
        "First Entry": None,
        "Registration: choose language": None,
        "Registration. Choose grade": None,
        "Registration. Choose lang group": None,
        "Registration. Choose exam group": None,
        "Registration": None,
        "Menu: cmd": None,
        "Back Handler": None,
        "HW ADD: attachments": None,
        "HW ADD: text": None,
        "HW ADD: final": None
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
        #logger.debug("Loading handler: %s" % i)

    for i in at_final:
        at_final[i].load(bot)
        logger.debug("Loading FINAL handler: %s" % i)

    logger.info(f"Handlers loaded: {handlers_count}.")


async def setup_middlewares(bot):
    middlewares_count = 0

    bot.labeler.message_event_view.register_middleware(OutdatedEventMiddleware())
    bot.labeler.message_event_view.register_middleware(EventAnswerMiddleware())

    for i in middlewares:
        bot.labeler.message_view.register_middleware(i)
        logger.debug(f"Loading middleware: %s." % i)
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
    Api.api = bot.api
    #storage = CtxStorage()
    #storage.set("api", bot.api)
    pass
