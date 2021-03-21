from entity import Entity


class World:
    top: int
    entities: dict[int, Entity]

    def __init__(self):
        self.entities = {}
        self.top = 0
