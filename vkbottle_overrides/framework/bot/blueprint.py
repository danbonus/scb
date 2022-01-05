from typing import Optional, Union
from vkbottle.api import ABCAPI, API
from vkbottle.polling import ABCPolling

from vkbottle_overrides.dispatch import ABCStateDispenser, BotRouter
from vkbottle_overrides.framework.abc_blueprint import ABCBlueprint
from vkbottle_overrides.framework.bot.bot import Bot
from vkbottle_overrides.framework.bot.labeler import SCBLabeler
from vkbottle_overrides.tools.dev_tools.loop_wrapper import LoopWrapper


class BotBlueprint(ABCBlueprint):
    def __init__(
        self,
        name: Optional[str] = None,
        labeler: Optional[SCBLabeler] = None,
        router: Optional[BotRouter] = None,
    ):
        if name is not None:
            self.name = name

        self.labeler = labeler or SCBLabeler()
        self.router: BotRouter = router or BotRouter()
        self.constructed = False
        self.loop_wrapper: LoopWrapper = ...
        self.handlers = None

    def construct(
        self, api: Union[ABCAPI, API], polling: ABCPolling, state_dispenser: ABCStateDispenser, loop_wrapper: LoopWrapper, handlers
    ) -> "BotBlueprint":
        self.api = api
        self.polling = polling
        self.state_dispenser = state_dispenser
        self.constructed = True
        self.loop_wrapper = loop_wrapper
        self.handlers = handlers
        return self

    def load(self, framework: "Bot") -> "BotBlueprint":
        framework.labeler.load(self.labeler)  # type: ignore
        # logger.debug(f"Blueprint {self.name!r} loaded")
        return self.construct(framework.api, framework.polling, framework.state_dispenser, framework.loop_wrapper, {i.handler.__name__: i for i in framework.labeler.message_view.handlers})

    @property
    def on(self) -> SCBLabeler:
        return self.labeler
