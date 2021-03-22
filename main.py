from commands import *
from context import *
from world import *


def parse_command(ctx: Context, args: str):
    command = args.split(" ")
    if len(command) == 0:
        return
    if handler := {"say": say, "summon": summon, "kill": kill}.get(command[0]):
        handler(ctx, ' '.join(command[1:]))


if __name__ == "__main__":  # cli
    world = World()
    ctx = Context.server(world)
    while True:
        query = input(">>> ")
        parse_command(ctx, query)
