from dataclasses import dataclass
from util.identifier import Identifier
from args import Converter, StrIterator
from typing import Set, Tuple, Optional

from context import Context
from entity import Entity

@dataclass
class OneEntityException(Exception): pass

@dataclass
class Selector(Converter):
    ty: str
    args: Set[Tuple[str, str]]
    # @implements Converter
    @staticmethod
    def convert(arg: StrIterator) -> Selector:
        if next(arg) != '@': arg.invalid("Expected '@'")
        ty = next(arg)
        if ty not in ('spear'): arg.invalid(f"Unknown selector type '{ty}'")
        args = set()
        match arg.peek():
            case '[':
                next(arg)
                while True:
                    lhs = ''
                    current = next(arg)
                    while current != '=':
                        lhs += current
                        current = next(arg)
                    rhs = ''
                    current = next(arg)
                    while current not in (',', ']'):
                        rhs += current
                        current = next(arg)
                    args.add((lhs, rhs))
                    if current == ']': break

        return Selector(ty, args)

    def apply(self, context: Context) -> list[Entity]:
        match self.ty:
            case 's': entities = [context.target] if context.target else []
            case 'e': entities = list(context.world.entities.values())
            case _: entities = []
        for ty in filter(lambda a: a[0] == "type", self.args):
            entities = list(filter(lambda e: e.ty == Identifier.new(ty[1]), entities))
        return entities

    def apply_one(self, context: Context) -> Optional[Entity]:
        matching = self.apply(context)
        if len(matching) > 1:
            raise OneEntityException()
        return matching[0] if len(matching) == 1 else None
