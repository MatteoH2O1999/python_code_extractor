import json
import pickle

from typing import Callable, Type, Union

from ..extractor.extract import extract_code
from ..loader.load import load_code


class _ReadableFileobj:
    def read(self, __n: int) -> bytes:
        ...

    def readline(self) -> bytes:
        ...


class _WritableFileobj:
    def write(self, __b: bytes) -> object:
        ...


def dumps(
    obj: Union[object, Type[object], Callable[..., object]],
    protocol: int = pickle.DEFAULT_PROTOCOL,
    fix_imports: bool = True,
) -> bytes:
    return pickle.dumps(
        obj=extract_code(obj), protocol=protocol, fix_imports=fix_imports
    )


def dump(
    obj: Union[object, Type[object], Callable[..., object]],
    file: _WritableFileobj,
    protocol: int = pickle.DEFAULT_PROTOCOL,
    fix_imports: bool = True,
) -> None:
    pickle.dump(
        obj=extract_code(obj), file=file, protocol=protocol, fix_imports=fix_imports
    )


def loads(
    string: bytes,
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
) -> Union[Type[object], Callable[..., object]]:
    json_string = pickle.loads(
        string, fix_imports=fix_imports, encoding=encoding, errors=errors
    )
    try:
        json.loads(json_string)
    except ValueError:
        raise ValueError("Passed bytes were not pickled by code_extractor")
    return load_code(json_string)


def load(
    file: _ReadableFileobj,
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
) -> Union[Type[object], Callable[..., object]]:
    json_string = pickle.load(
        file=file, fix_imports=fix_imports, encoding=encoding, errors=errors
    )
    try:
        json.loads(json_string)
    except ValueError:
        raise ValueError("Specified file was not pickled by code_extractor")
    return load_code(json_string)
