import os
import argparse

from logger import logger
from vkbottle import CtxStorage

from repositories import SettingsRepository
from bot import init_bot


if __name__ == '__main__':
    storage = CtxStorage(default={"user_token": os.environ.get("user_token")})

    parser = argparse.ArgumentParser(description='SCB')

    parser.add_argument('--debug', type=bool,
                        help='Debug mode')

    args = parser.parse_args()

    settings = SettingsRepository(args.debug)
    scb = init_bot(settings.token)
    scb.loop_wrapper.on_startup.insert(0, settings.check_group_id(scb.api))
    scb.run_forever()
