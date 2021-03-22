from dataclasses import dataclass
from args import Converter, InvalidChar, StrIterator
from util.identifier import Identifier


@dataclass
class Entity(Converter):
    ty: Identifier
    name: str
    uuid: int

    # @implements Converter
    @staticmethod
    def convert(arg: StrIterator) -> Entity:
        id_s = ""
        current = arg.peek()
        ident_start = arg.index
        while current not in (None, " "):
            current = next(arg)
            id_s += current
            current = arg.peek()
        id = Identifier.new(id_s)
        if id == None: raise InvalidChar(ident_start, "Invalid identifier")
        return Entity(ty=id, name=id.name.capitalize(), uuid=0)
