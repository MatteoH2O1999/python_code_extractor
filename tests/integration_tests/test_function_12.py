import inspect
import os
import numpy as np
import warnings

from numpy import mean

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


TEST_GLOBAL_VARIABLE = np.arange(0, 6, 1)
TEST_GLOBAL_DICT = {"test": 5, "test2": 3}
TEST_GLOBAL_FLOAT = 42.69


def function_12():
    return mean(TEST_GLOBAL_VARIABLE), TEST_GLOBAL_DICT, TEST_GLOBAL_FLOAT


def test_extract_function_with_global_variable():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_12.json")
    ) as json_file:
        json_txt = json_file.read()
    with warnings.catch_warnings(record=True) as w:
        expected_code = ExtractedCode.from_string(json_txt)
        extracted_code = ExtractedCode.from_string(extract_code(function_12))
        assert extracted_code.name == expected_code.name
        assert extracted_code.code == expected_code.code
        assert extracted_code.imports == expected_code.imports
        assert len(w) == 3
        for warning in w:
            assert (
                "Will fallback to pickle the value but compatibility with different versions is not guaranteed."
                in str(warning.message)
            )
        expected_dict = {}
        for imp in expected_code.imports:
            exec(imp, expected_dict)
        for dep in expected_code.dependencies:
            exec(dep, expected_dict)
        extracted_dict = {}
        for imp in extracted_code.imports:
            exec(imp, extracted_dict)
        for dep in extracted_code.dependencies:
            exec(dep, extracted_dict)
        np.testing.assert_equal(extracted_dict, expected_dict)


def test_load_function_with_global_variable():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_12.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_12"
    assert extracted_method() == (
        mean(TEST_GLOBAL_VARIABLE),
        TEST_GLOBAL_DICT,
        TEST_GLOBAL_FLOAT,
    )