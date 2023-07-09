import enum
from enum import Enum, auto, unique


dummy_dict = {"a": [0, 1, 2], "b": [3, 4, 5]}


@unique
class DummyEnum(Enum):
    Dummy1 = auto()
    Dummy2 = auto()
    Dummy3 = auto()


@enum.unique
class DummyEnum(enum.Enum):
    Dummy1 = enum.auto()
    Dummy2 = enum.auto()
    Dummy3 = enum.auto()
