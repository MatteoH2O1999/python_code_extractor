import inspect
import os
import numpy as np

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import _ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def function_3():
    return np.mean


def test_extract_third_party_closure_alias_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_3.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(function_3))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_third_party_closure_alias_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_3.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_3"
    assert extracted_method() is np.mean
