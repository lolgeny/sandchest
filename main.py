from commands import *
from context import *
from world import *


def parse_command(ctx: Context, command: str, *args: str):
    if handler := {
        "say": say,
        "summon": summon,
        "kill": kill
    }.get(command):
        handler(ctx, *args)


if __name__ == "__main__":  # cli
    world = World()
    ctx = Context.server(world)
    while True:
        query = input(">>> ")
        parse_command(ctx, *query.split(" "))
