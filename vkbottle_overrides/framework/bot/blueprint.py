from typing import Optional

from vkbottle.dispatch import BotRouter
from vkbottle.bot import Blueprint

from vkbottle_overrides.framework.bot.labeler import SCBLabeler


class BotBlueprint(Blueprint):
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
