from dataclasses import dataclass
from util.identifier import Identifier
from args import Converter
from typing import Optional

from context import Context
from entity import Entity

@dataclass
class Selector(Converter):
    ty: str
    args: dict[str, str]
    # @implements Converter
    @staticmethod
    def convert(arg: str) -> Optional[Selector]:
        if len(arg) < 2 or arg[0] != '@': return None
        ty = arg[1]
        if ty not in ('spear'): return None
        args = {}
        if len(arg) > 2:
            if arg[2] != '[' or arg[-1] != ']': return None
            raw_args = arg[3:-1].replace(' ', '').split(',')
            for arg in raw_args:
                parts = arg.split('=')
                if len(parts) != 2: return None
                args[parts[0]] = parts[1]
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