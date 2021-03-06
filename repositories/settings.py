from configparser import ConfigParser
from distutils.util import strtobool

from motor.motor_asyncio import AsyncIOMotorClient
from vkbottle import API

from logger import logger_debug, logger
from repositories import GradesRepository
from repositories.repository import Repository
from utils.api import Api
from vkbottle_overrides.tools import CtxStorage


class SettingsRepository:
    """СТРОКИ В КОНФИГЕ ВСЕГДА БЕЗ КАВЫЧЕК!"""

    def __init__(self, mode):
        self.mode = mode

        if mode is None:
            self.mode = "prod"

        self.storage = CtxStorage()
        self.motor = AsyncIOMotorClient(f'mongodb://localhost:27017/scb')
        self.config, self.section = self.get_settings()
        self.token = self.get("token")
        self.user_token = self.get("user_token")
        Api.user_api = API(self.user_token)
        self.service_token = self.get("service_token")
        self.init_group_id = self.config.getint(self.section, "init_group_id")
        self.db = self.get("db")
        self.db = self.motor[self.db]
        self.storage.set("db", self.db)
        Repository.db = self.db

    def get_settings(self):
        config = ConfigParser()
        config.read("config.ini")

        if config.getboolean("bot", "debug"):
            self.mode = "debug"
            logger_debug()

        if self.mode == "prod":
            section = "credentials"
        else:
            section = "dev_credentials"

        return config, section

    def get(self, value):
        result = self.config.get(self.section, value)
        self.storage.set(value, result)

        return result

    def set(self, key, value):
        self.config.set(self.section, key, str(value))

    async def check_group_id(self, api):
        api = Api(api)
        group_id = await api.get_group_id()
        Api.group_id = group_id

        if self.init_group_id:
            '''if group_id != self.init_group_id:
                logger.error("You've changed the bot group. 'Y' to refresh the grades DB (album IDs change).")
                try:
                    if strtobool(input()):
                        await GradesRepository.refresh_grades()
                        return
                except ValueError:
                    pass

                exit(-1)'''
        else:
            logger.info("First start! Saving the group id.")
            self.set("init_group_id", group_id)
            with open("config.ini", "w") as config_file:
                self.config.write(config_file)
