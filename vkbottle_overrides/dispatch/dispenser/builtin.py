from typing import Dict, Union, Optional

from models.state import BaseStateGroup, StatePeer

from .abc import ABCStateDispenser

import itertools

from logger import logger

class BuiltinStateDispenser(ABCStateDispenser):
    def __init__(self):
        self.dictionary: Dict[int, StatePeer] = {}

    async def get(self, peer_id: int) -> Optional[StatePeer]:
        return self.dictionary.get(peer_id)

    async def set(self, peer_id: int, state: Union[BaseStateGroup, str], **payload):
        logger.debug("Setting state: %s" % state)

        last_state = await self.get(peer_id)
        if not last_state:
            logger.debug("State not found. Creating zero-state")
            last_state = await self.set_tree(peer_id, None, None)

        self.dictionary[peer_id] = StatePeer(
            peer_id=peer_id, state=state, payload=payload, tree=last_state.tree
        )

    async def set_tree(self, peer_id, handler, message):
        current_state = await self.get(peer_id)
        print("Setting fucking TREE!")
        if current_state and current_state.state != 0:
            print(current_state.state)
            print([i for i in current_state.tree])
            if current_state.state in current_state.tree:
                print("Reverting state!")
                index = list(current_state.tree).index(current_state.state)
                print(current_state.state)
                print(list(current_state.tree)[-1])
                if current_state.state == list(current_state.tree)[-1]:
                    print("FUCK IT")
                    return
                tree = dict(itertools.islice(current_state.tree.items(), index))
                current_state.state = list(tree)[-1]
                if len(tree) == 1:
                    tree = {0: {"handler": handler, "message": message}}
                    current_state = StatePeer(
                        peer_id=peer_id, state=0, payload=None, tree=tree
                    )
            else:
                print("No reverting. Going straight forward!")
                print(current_state.tree)
                tree = current_state.tree
                tree[current_state.state] = {"handler": handler, "message": message}
            current_state.tree = tree
        else:
            print("No old state!")
            tree = {0: {"handler": handler, "message": message}}
            current_state = StatePeer(
            peer_id=peer_id, state=0, payload=None, tree=tree
        )

        self.dictionary[peer_id] = current_state

        print("Tree: %s" % [i for i in tree])
        return current_state


    async def delete(self, peer_id: int):
        print("removing a state")
        self.dictionary.pop(peer_id)
