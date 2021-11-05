import argparse

from logger import logger
from vkbottle_overrides.tools import CtxStorage

from repositories import SettingsRepository
from bot import init_bot


async def beu():
    print("сработало")


if __name__ == '__main__':
    storage = CtxStorage()

    parser = argparse.ArgumentParser(description='SCB')

    parser.add_argument('--debug', type=bool,
                        help='Debug mode')

    args = parser.parse_args()

    settings = SettingsRepository(args.debug)
    scb = init_bot(settings.token)
    scb.loop_wrapper.on_startup.insert(0, settings.check_group_id(scb.api))
    scb.run_forever()
