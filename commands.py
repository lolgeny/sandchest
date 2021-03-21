from args import *
from context import *
from util.selector import Selector


@args
def say(ctx: Context, *args: str):
    print(f"[{ctx.target.name if ctx.target else '@'}] ", end="")
    for word in args:
        if len(word) > 0 and word[0] == "@":
            if sel := Selector.convert(word):
                print(", ".join(map(lambda e: e.name, sel.apply(ctx))), end='')
                continue
        print(word, end=" ")
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