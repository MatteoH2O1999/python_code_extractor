import pickle

from typing import Callable, TextIO, Type, Union


def dumps(
    obj: Union[Type[object], Callable[..., object]],
    protocol: int = pickle.DEFAULT_PROTOCOL,
) -> str:
    return ""


def dump(
    obj: Union[Type[object], Callable[..., object]],
    file: TextIO,
    protocol: int = pickle.DEFAULT_PROTOCOL,
) -> None:
    pass


def loads(string: str) -> Union[Type[object], Callable[..., object]]:
    return object


def load(file: TextIO) -> Union[Type[object], Callable[..., object]]:
    return object
