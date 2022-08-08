import os

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
    extracted_code = extract_code(function_1, install_missing=False)
    assert extracted_code == expected_code
