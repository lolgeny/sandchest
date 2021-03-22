from dataclasses import dataclass
from util.identifier import Identifier
from args import Converter, StrIterator

from context import Context
from entity import Entity

@dataclass
class Selector(Converter):
    ty: str
    args: dict[str, str]
    # @implements Converter
    @staticmethod
    def convert(arg: StrIterator) -> Selector:
        if next(arg) != '@': arg.invalid("Expected '@'")
        ty = next(arg)
        if ty not in ('spear'): arg.invalid(f"Unknown selector type '{ty}'")
        args = {}
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
                    args[lhs] = rhs
                    if current == ']': break

        return Selector(ty, args)

    def apply(self, context: Context) -> list[Entity]:
        match self.ty:
            case 's': entities = [context.target] if context.target else []
            case 'e': entities = list(context.world.entities.values())
            case _: entities = []
        if "type" in self.args:
            if ty := Identifier.new(self.args["type"]):
                entities = filter(lambda e: e.ty == ty, entities)
        return list(entities)