from typing import Callable, Type, Union

from ..extracted_code import ExtractedCode


def extract_code(
    obj: Union[Type[object], Callable[..., object]],
    install_missing: bool = False,
) -> str:
    return ""
