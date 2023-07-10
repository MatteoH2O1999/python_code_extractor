import enum
from enum import Enum, auto, unique


dummy_dict = {"a": [0, 1, 2], "b": [3, 4, 5], "c": "a"}


@unique
class DummyEnum(Enum):
    Dummy1 = auto()
    Dummy2 = auto()
    Dummy3 = auto()


@enum.unique
class DummyEnumModule(enum.Enum):
    Dummy1 = enum.auto()
    Dummy2 = enum.auto()
    Dummy3 = enum.auto()


variable_key = "key"
variable_value = 42

dummy_dict_enum = {
    DummyEnum.Dummy2: 5,
    DummyEnumModule.Dummy3: 1,
    variable_key: variable_value,
}
