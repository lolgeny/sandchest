from typing import Optional
from dataclasses import dataclass


@dataclass
class Identifier:
    namespace: str
    parts: list[str]
    name: str

    @staticmethod
    def new(id: str) -> Optional[Identifier]:
        sub = id.split(":")
        if len(sub) > 2:
            return None
        if len(sub) < 2:
            sub.insert(0, "minecraft")
        parts = sub[1].split("/")
        return Identifier(namespace=sub[0], parts=parts[:-1], name=parts[-1])
