from entity import Entity
from world import World

from typing import Optional


class Context:
    target: Optional[Entity]
    world: World

    @staticmethod
    def server(world: World) -> Context:
        self = Context()
        self.target = None
        self.world = world
        return self
