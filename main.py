import os
import argparse
from distutils.util import strtobool

from logger import logger
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from vkbottle import CtxStorage
from repositories.grades import GradesRepository
from configparser import ConfigParser

from repositories.grades import GradesRepository
from bot import init_bot
from utils.api import Api


async def check_group_id():
    group_id = await Api(scb.api).get_group_id()

    if init_group_id:
        if group_id != init_group_id:
            logger.error("You've changed the bot group. Am i supposed to refresh Grades DB? (Y/N)")
            try:
                prompt = strtobool(input())
                if prompt:
                    await GradesRepository.refresh_grades()

                else:
                    logger.critical("Sorry, there'll be error.")
                    exit(-1)

            except ValueError:
                logger.critical("Write something else, dude.")

    else:
        logger.debug("Setting the init group id")
        config.set("bot", option, str(group_id))
        with open("config.ini", "w") as config_file:
            config.write(config_file)

load_dotenv("credentials.env")
url = os.environ.get("url")

config = ConfigParser()
config.read("config.ini")
option = "init_group_id"
init_group_id = config.getint("bot", option)

client = AsyncIOMotorClient(f'mongodb://{url}')

defaults = {
    "debug": True,
    "db": client.scb,
    "token": os.environ.get("scb_token"),
    "user_token": os.environ.get("user_token")
}


if __name__ == '__main__':
    storage = CtxStorage(default=defaults)

    parser = argparse.ArgumentParser(description='SCB')

    parser.add_argument('--debug', type=bool,
                        help='Debug mode')

    args = parser.parse_args()
    print(args)
    if args.debug or defaults["debug"]:
        storage.set("db", client.scbdev)
        storage.set("token", os.environ.get("dev_scb_token"))
        option = "dev_init_group_id"
        init_group_id = config.getint("bot", "dev_init_group_id")

    scb = init_bot(storage.get("token"))
    scb.loop_wrapper.on_startup.insert(0, check_group_id())
    scb.run_forever()
