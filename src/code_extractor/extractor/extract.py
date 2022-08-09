import inspect
from typing import Callable, Type, Union

from ..extracted_code import ExtractedCode


def extract_code(obj: Union[object, Type[object], Callable[..., object]]) -> str:
    if not inspect.isclass(obj):
        obj = obj.__class__
    return _extract_code(obj).to_string()


def _extract_code(obj: Union[Type[object], Callable[..., object]]) -> ExtractedCode:
    return ExtractedCode()
