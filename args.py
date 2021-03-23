from inspect import signature, Parameter
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
        if c := self.peek():
            self.index += 1
            return c
        else:
            raise ExpectedChar(self.index)

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


class Word(Converter):
    # @implements Converter
    @staticmethod
    def convert(args: StrIterator) -> str:
        word = ''
        if args.empty() or args.peek() == ' ':
            args.invalid("Expected word")
        while not args.empty() and not args.peek() == " ":
            word += next(args)
        return word

def selection(*valid: str):
    class Selection(Word):
        # @implements Converter
        # @overrides Word
        @staticmethod
        def convert(args: StrIterator) -> str:
            word = Word.convert(args)
            if word not in valid:
                args.invalid(f"Expected one of {valid}")
            return word
    return Selection

def args(f: Callable) -> Callable:
    sig = signature(f)
    args = filter(lambda p: p[1].kind == Parameter.POSITIONAL_OR_KEYWORD, sig.parameters.items())
    next(args)
    kw = list(filter(lambda p: p[1].kind == Parameter.KEYWORD_ONLY, sig.parameters.items()))
    converters = []
    has_args = False
    for arg, details in args:
        has_args = True
        converter = details.annotation
        # assert isinstance(converter, Converter)
        converters.append(converter.convert)

    l = len(converters)
    match len(kw):
        case 0: rest = False
        case 1: rest = True
        case _: raise SyntaxError("Can only have one greedy string in command")

    def arg_function(*argsl, empty: bool = True):
        ctx = argsl[-2]
        args: StrIterator = argsl[-1]
        parsed_args = []
        for i in range(l):
            parsed = converters[i](args)
            parsed_args.append(parsed)
            if not args.empty() and next(args) != " ":
                args.invalid("Expected space")

        ctx._redirect = args

        built_args = list(argsl[:-1])
        built_args.extend(parsed_args)
        if rest:
            i = args.index
            args.index = len(args._base)
            f(*built_args, **{kw[0][0]: args._base[i:]})
        else:
            f(*built_args)
            if empty and not args.empty():
                args.unexpected()
    return arg_function
