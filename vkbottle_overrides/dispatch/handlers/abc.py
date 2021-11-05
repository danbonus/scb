from abc import ABC, abstractmethod
from typing import Any, Union, Callable


class ABCHandler(ABC):
    blocking: bool

    def __init__(self):
        self.handler = Callable

    @abstractmethod
    async def filter(self, event: Any, scb) -> Union[dict, bool]:
        pass

    @abstractmethod
    async def handle(self, event: Any, scb, **context) -> Any:
        pass
