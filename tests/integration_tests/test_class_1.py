import inspect
import os

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import _ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Class1:
    def method(self):
        return "Test method"


def test_extract_isolated_class():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_1.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(Class1))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_extract_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_1.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(Class1()))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_isolated_class():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_1.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_class = load_code(json_txt)
    instance = extracted_class()
    assert inspect.isclass(extracted_class)
    assert extracted_class.__name__ == "Class1"
    assert hasattr(instance, "method")
    assert inspect.ismethod(getattr(instance, "method", None))
    assert getattr(instance, "method", None)() == "Test method"


def test_extract_method_isolated_class():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_1_method.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(Class1.method))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_extract_method_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_1_method.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(Class1().method))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_method_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_1_method.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "method"
    assert extracted_method(None) == "Test method"
