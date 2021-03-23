from commands import *
from context import *
from world import *
from args import StrIterator


def parse_command(ctx: Context, args: str):
    command(ctx, StrIterator(args))
    # command = args.split(" ")
    # if len(command) == 0:
        # return
    # if handler := {"say": say, "summon": summon, "kill": kill, "data": data}.get(command[0]):
        # handler(ctx, StrIterator(' '.join(command[1:])))


if __name__ == "__main__":  # cli
    world = World()
    ctx = Context.server(world)
    while True:
        query = input(">>> ")
        parse_command(ctx, query)
