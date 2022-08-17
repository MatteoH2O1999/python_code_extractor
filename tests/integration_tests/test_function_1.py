import inspect
import os
import subprocess
import sys

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def function_1():
    return "Test return"


def test_extract_isolated_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_1.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(function_1))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_extract_isolated_function_with_requirements():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_1.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(
        extract_code(function_1, get_requirements=True)
    )
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports
    expected_requirements = set(
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE)
        .stdout.decode(encoding="utf-8")
        .splitlines(keepends=False)
    )
    assert extracted_code.requirements == expected_requirements


def test_load_isolated_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_1.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_1"
    assert extracted_method() == "Test return"
