import os
import numpy
import numpy as np

from code_extractor import extract_code
from code_extractor.extracted_code import ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


######################################################
#                 Test function 1                    #
######################################################


def function_1():
    print("test function 1")


def test_extract_isolated_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_1.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(function_1))
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


######################################################
#                 Test function 2                    #
######################################################


def function_2():
    return numpy.mean


def test_extract_third_party_closure_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_2.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(function_2))
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


######################################################
#                 Test function 3                    #
######################################################


def function_3():
    return np.mean


def test_extract_third_party_closure_alias_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_3.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(function_3))
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports
