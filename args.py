from inspect import getfullargspec
from abc import ABC, abstractmethod
from typing import Callable, Optional


class Converter(ABC):
    @staticmethod
    @abstractmethod
    def convert(arg: str) -> Optional[object]:
        pass


def args(f: Callable) -> Callable:
    args, _, _, _, _, _, annotations = getfullargspec(f)
    converters = []
    for arg in args[1:]:
        converter = annotations[arg]
        # assert isinstance(converter, Converter)
        converters.append(converter.convert)

    def arg_function(self, *args_t: str):
        args = list(args_t)
        parsed_args = []
        for i in range(len(converters)):
            parsed = converters[i](args.pop(0))
            if parsed == None:
                assert 3 == 4
            parsed_args.append(parsed)
        f(self, *parsed_args, *args)

    return arg_function
