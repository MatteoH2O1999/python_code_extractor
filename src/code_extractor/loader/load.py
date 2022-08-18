"""
Module containing code for loading the source code extracted from live python objects.
"""
import inspect

from typing import Callable, Type, Union

from ..extracted_code import _ExtractedCode


def load_code(code: str) -> Union[Type[object], Callable[..., object]]:
    """
    Load the provided source code and return the previously extracted class or function.
    Note that only strings extracted with this package are guaranteed to be restored.
    No guarantees are given with arbitrary strings (this package makes use of exec,
    only use strings whose origin you trust).

    :param code: The extracted code.
    :type code: str
    :return: The extracted class or function.
    :rtype: type(object), Callable[..., object]
    """
    extracted_code = _ExtractedCode.from_string(code)
    global_dict = {}
    exec(extracted_code.to_code(), global_dict)
    if extracted_code.name not in global_dict.keys():
        raise RuntimeError(
            f"Sanity check failed. Expected {extracted_code.name} to be in global dict {global_dict}."
        )
    to_return = global_dict[extracted_code.name]
    if to_return is None:
        raise RuntimeError(
            f"Sanity check failed. Expected global_dict[{extracted_code.name}] to not be None."
        )
    if inspect.isclass(to_return) or isinstance(to_return, Callable):
        return to_return
    raise RuntimeError(
        f"Sanity check failed. Expected global_dict[{extracted_code.name}] to be either of "
        f"type Type[object] or Callable[..., object], got {type(to_return)}"
    )
