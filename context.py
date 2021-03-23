from args import StrIterator
from entity import Entity
from world import World

from typing import Optional, Callable


class Context:
    target: Optional[Entity]
    world: World

    @staticmethod
    def server(world: World) -> Context:
        self = Context()
        self.target = None
        self.world = world
        return self

    def copy(self) -> Context:
        copy = Context()
        copy.target = self.target
        copy.world = self.world
        copy._redirect = self._redirect
        return copy

    _redirect: Optional[StrIterator]

    def redirect(self, to: Callable, *args, empty: bool = True): # used in functions to keep parsing
        if s := self._redirect:
            if len(args) > 0:
                return to(*args, self, s, empty=empty)
            else:
                return to(self, s, empty=empty)
        else:
            raise NotImplementedError
