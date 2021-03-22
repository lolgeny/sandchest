from args import *
from context import *
from util.selector import Selector


@args
def say(ctx: Context, *, args: str):
    print(f"[{ctx.target.name if ctx.target else '@'}] ", end="")
    it = StrIterator(args)
    while c := it.peek():
        if c == "@":
            s = Selector.convert(it)
            print(f"[{', '.join(map(lambda e: e.name, s.apply(ctx)))}]", end="")
        else:
            next(it)
            print(c, end="")
    print()


@args
def summon(ctx: Context, entity: Entity):
    entity.uuid = ctx.world.top
    ctx.world.entities[ctx.world.top] = entity
    ctx.world.top += 1


@args
def kill(ctx: Context, target: Selector):
    for dead in target.apply(ctx):
        del ctx.world.entities[dead.uuid]
