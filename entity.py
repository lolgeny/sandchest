from dataclasses import dataclass
from args import Converter
from typing import Optional
from util.identifier import Identifier


@dataclass
class Entity(Converter):
    ty: Identifier
    name: str
    uuid: int

    # @implements Converter
    @staticmethod
    def convert(arg: str) -> Optional[Entity]:
        id = Identifier.new(arg)
        if id == None:
            return None
        return Entity(ty=id, name=id.name.capitalize(), uuid=0)
