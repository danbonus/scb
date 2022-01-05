from enum import IntEnum

from pydantic import BaseModel
from typing import Tuple, Type, Union


class BaseStateGroup(IntEnum):
    pass


class StatePeer(BaseModel):
    peer_id: int
    state: int
    payload: Union[dict, None]
    tree: Union[dict, None]

    def get_state_path(self) -> Tuple[Type[BaseStateGroup], BaseStateGroup]:
        return self.state.__class__, self.state

    def get_state_repr(self) -> str:
        state_group, index = self.get_state_path()
        return f"{state_group.__name__}_{index}"
