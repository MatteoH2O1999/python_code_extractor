"""
Module containing code to expose pickle-like API
"""
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
    """
    Return the pickled representation of the object obj as a bytes object, instead of writing it to a file.

    :param obj: The object to pickle
    :type obj: object, type(object), Callable[..., object]
    :param protocol: Tells the pickler to use the given protocol;
        supported protocols are 0 to HIGHEST_PROTOCOL.
        If not specified, the default is DEFAULT_PROTOCOL.
        If a negative number is specified, HIGHEST_PROTOCOL is selected.
    :type protocol: int
    :param fix_imports: If fix_imports is True and protocol is less than 3,
        pickle will try to map the new Python 3 names to the old module names
        used in Python 2, so that the pickle data stream is readable with Python 2.
    :type fix_imports: bool
    :return: The written bytes
    :rtype: bytes
    """
    return pickle.dumps(
        obj=extract_code(obj), protocol=protocol, fix_imports=fix_imports
    )


def dump(
    obj: Union[object, Type[object], Callable[..., object]],
    file: _WritableFileobj,
    protocol: int = pickle.DEFAULT_PROTOCOL,
    fix_imports: bool = True,
) -> None:
    """
    Write the pickled representation of the object obj to the open file object file.

    :param obj: The object to pickle
    :type obj: object, type(object), Callable[..., object]
    :param file: It must have a write() method that accepts a single bytes argument.
        It can thus be an on-disk file opened for binary writing, an io.BytesIO instance,
        or any other custom object that meets this interface.
    :type file: _WritableFileobj
    :param protocol: Tells the pickler to use the given protocol;
        supported protocols are 0 to HIGHEST_PROTOCOL.
        If not specified, the default is DEFAULT_PROTOCOL.
        If a negative number is specified, HIGHEST_PROTOCOL is selected.
    :type protocol: int
    :param fix_imports: If fix_imports is True and protocol is less than 3,
        pickle will try to map the new Python 3 names to the old module names
        used in Python 2, so that the pickle data stream is readable with Python 2.
    :type fix_imports: bool
    """
    pickle.dump(
        obj=extract_code(obj), file=file, protocol=protocol, fix_imports=fix_imports
    )


def loads(
    string: bytes,
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
) -> Union[Type[object], Callable[..., object]]:
    """
    Return the reconstituted object hierarchy of the pickled representation string of an object.
    string must be a bytes-like object.

    The protocol version of the pickle is detected automatically, so no protocol argument is needed.
    Bytes past the pickled representation of the object are ignored.

    Note only strings generated with this package's dumps method can be unpickled.

    :param string: The data to unpickle.
    :type string: bytes
    :param fix_imports: If true, pickle will try to map the old Python 2 names
        to the new names used in Python 3.
    :type fix_imports: bool
    :param encoding: Specify bytes encoding for Python 2 compatibility.
    :type encoding: str
    :param errors: Specify error handling.
    :type errors: str
    :return: The unpickled object
    :rtype: type(object), Callable[..., object]
    """
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
    """
    Read the pickled representation of an object from the open file object
    file and return the reconstituted object hierarchy specified therein.

    The protocol version of the pickle is detected automatically,
    so no protocol argument is needed. Bytes past the pickled
    representation of the object are ignored.

    Note only files written with this package's dump method can be unpickled.

    :param file: It must have three methods, a read() method that takes an integer argument,
        a readinto() method that takes a buffer argument and a readline() method that requires
        no arguments, as in the io.BufferedIOBase interface. Thus file can be an on-disk file
        opened for binary reading, an io.BytesIO object, or any other custom object that meets
        this interface.
    :type file: _ReadableFileobj
    :param fix_imports: If true, pickle will try to map the old Python 2 names
        to the new names used in Python 3.
    :type fix_imports: bool
    :param encoding: Specify bytes encoding for Python 2 compatibility.
    :type encoding: str
    :param errors: Specify error handling.
    :type errors: str
    :return: The unpickled object
    :rtype: type(object), Callable[..., object]
    """
    json_string = pickle.load(
        file=file, fix_imports=fix_imports, encoding=encoding, errors=errors
    )
    try:
        json.loads(json_string)
    except ValueError:
        raise ValueError("Specified file was not pickled by code_extractor")
    return load_code(json_string)
