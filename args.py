from inspect import getfullargspec
from abc import ABC, abstractmethod
from typing import Callable, Optional
from dataclasses import dataclass


@dataclass
class ExpectedChar(Exception):
    position: int


@dataclass
class InvalidChar(Exception):
    position: int
    message: str

@dataclass
class UnexpectedChar(Exception):
    position: int


class StrIterator:
    _base: str
    index: int

    def __init__(self, base: str):
        self._base = base
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        self.index += 1
        if self.index > len(self._base):
            raise ExpectedChar(self.index)
        else:
            return self._base[self.index - 1]

    def peek(self) -> Optional[str]:
        if self.index >= len(self._base):
            return None
        else:
            return self._base[self.index]

    def empty(self) -> bool:
        return self.index >= len(self._base)

    def invalid(self, message: str):
        raise InvalidChar(self.index, message)

    def unexpected(self):
        raise UnexpectedChar(self.index)


class Converter(ABC):
    @staticmethod
    @abstractmethod
    def convert(args: StrIterator) -> object:
        pass


def args(f: Callable) -> Callable:
    args, _, _, _, kw, _, annotations = getfullargspec(f)
    converters = []
    for arg in args[1:]:
        converter = annotations[arg]
        # assert isinstance(converter, Converter)
        converters.append(converter.convert)

    l = len(converters)
    match len(kw):
        case 0: rest = False
        case 1: rest = True
        case _: raise SyntaxError("Can only have one greedy string in command")

    has_args = len(args) > 1

    def arg_function(self, args_s: str):
        args = StrIterator(args_s)
        parsed_args = []
        for i in range(l):
            parsed = converters[i](args)
            if parsed == None:
                assert 3 == 4
            parsed_args.append(parsed)
            if i != l - 1 and next(args) != " ":
                assert 4 == 5
        if rest:
            if has_args:
                f(self, *parsed_args, **{kw[0]: args._base[args.index:]})
            else:
                f(self, **{kw[0]: args._base[args.index:]})
        else:
            if not args.empty(): args.unexpected()
            if has_args:
                f(self, *parsed_args)
            else:
                f(self)

    return arg_function
