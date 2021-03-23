from args import *
from context import *
from util.selector import Selector
from typing import Optional

command: Optional[Callable] = None

@args
def say(ctx: Context, *, args: str):
    print(f"[{ctx.target.name if ctx.target else '@'}] ", end="")
    it = StrIterator(args)
    while c := it.peek():
        if c == "@":
            s = Selector.convert(it)
            entities = s.apply(ctx)
            names = map(lambda e: e.name, entities)
            print(f"[{', '.join(names) if len(entities) > 0 else ''}]", end="")
        else:
            next(it)
            print(c, end="")
    print()


@args
def summon(ctx: Context, entity: Entity):
    entity.nbt["UUID"] = ctx.world.top
    ctx.world.entities[ctx.world.top] = entity
    ctx.world.top += 1


@args
def kill(ctx: Context, target: Selector):
    for dead in target.apply(ctx):
        del ctx.world.entities[dead.uuid]

@args
def execute(ctx: Context, sub: selection('as', 'run')):
    assert command != None
    match sub:
        case 'as': ctx.redirect(execute_as),
        case 'run': ctx.redirect(command)

@args
def execute_as(ctx: Context, target: Selector):
    for e in target.apply(ctx):
        c = ctx.copy()
        c.target = e
        c.redirect(execute)


@args
def data(ctx: Context, operation: selection('merge')):
    target = ctx.redirect(data_target, empty=False)
    match operation:
        case 'merge':
            ctx.redirect(data_merge, target)

@args
def data_target(ctx: Context, target: selection('entity')) -> Entity:
    match target:
        case 'entity':
            return ctx.redirect(data_entity, empty=False)
    assert False

@args
def data_entity(ctx: Context, target: Selector) -> Optional[Entity]:
    return target.apply_one(ctx)

@args
def data_merge(target: Entity, /, ctx: Context):
    print('data merge')

commands = {
    "say": say, 
    "summon": summon, 
    "kill": kill, 
    "data": data,
    "execute": execute
}

@args
def command(ctx: Context, cmd: Word):
    assert isinstance(cmd, str)
    if cmd not in commands:
        print('ohno')
    ctx.redirect(commands[cmd])