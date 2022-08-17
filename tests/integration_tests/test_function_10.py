import inspect
import os

from numpy import mean

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import _ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def function_10():
    instance = DependencyClass()
    return instance.method()


class ParentClass:
    def __init__(self):
        self.dep = mean


class DependencyClass(ParentClass):
    def method(self):
        return self.dep


def test_extract_function_with_class_dependency():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_10.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(function_10))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_function_with_class_dependency():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_10.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_10"
    assert extracted_method() is mean
