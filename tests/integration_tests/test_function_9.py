import inspect
import os

from numpy.random import random
from numpy import mean

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def function_9():
    def nested():
        return random

    return nested, mean


def test_extract_external_function_dependency_nested_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_9.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(function_9))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_external_function_dependency_nested_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_9.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_9"
    return_tuple = extracted_method()
    assert isinstance(return_tuple, tuple)
    assert inspect.isfunction(return_tuple[0])
    assert return_tuple[0].__name__ == "nested"
    assert return_tuple[1] is mean
    assert return_tuple[0]() is random
