from dataclasses import dataclass
from args import Converter, InvalidChar, StrIterator
from util.identifier import Identifier

class Entity(Converter):
    ty: Identifier
    nbt: dict

    @property
    def uuid(self) -> int: return int(self.nbt["UUID"])

    @property
    def name(self) -> str: return str(self.nbt["CustomName"])

    def __init__(self, ty: Identifier):
        self.ty = ty
        self.nbt = {
            "CustomName": ty.name.capitalize(),
            "UUID": 0
        }

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
        return Entity(ty=id)
