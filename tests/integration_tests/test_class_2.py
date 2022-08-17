import inspect
import os

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Class2:
    @staticmethod
    def method(parameter):
        return parameter


def test_extract_static_isolated_class():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_2.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(Class2))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_extract_static_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_2.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(Class2()))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_static_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_2.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_class = load_code(json_txt)
    instance = extracted_class()
    assert inspect.isclass(extracted_class)
    assert extracted_class.__name__ == "Class2"
    assert hasattr(extracted_class, "method")
    assert inspect.isfunction(getattr(extracted_class, "method", None))
    assert hasattr(instance, "method")
    assert inspect.isfunction(getattr(instance, "method", None))
    assert getattr(extracted_class, "method", None)(42) == 42
    assert getattr(instance, "method", None)(69) == 69


def test_extract_static_method_isolated_class():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_2_method.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(Class2.method))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_extract_static_method_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_2_method.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(Class2().method))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_static_method_isolated_instance():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "class_2_method.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_static_method = load_code(json_txt)
    assert extracted_static_method.__name__ == "method"
    assert inspect.isfunction(extracted_static_method)
    assert extracted_static_method(42) == 42
