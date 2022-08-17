import inspect
import os
import numpy as np
import numpy.random

from numpy import mean
from numpy.random import random

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import ExtractedCode

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def function_11():
    return Dep1.dep1(), Dep1.dep2(), Dep2.dep1(), Dep2.dep2()


class Dep1:
    @staticmethod
    def dep1():
        return mean

    @staticmethod
    def dep2():
        return np


class Dep2:
    @staticmethod
    def dep1():
        return numpy.random

    @staticmethod
    def dep2():
        return random


def test_extract_function_with_class_dependency_from_static_method():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_11.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = ExtractedCode.from_string(json_txt)
    extracted_code = ExtractedCode.from_string(extract_code(function_11))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_function_with_class_dependency_from_static_method():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_11.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_11"
    assert extracted_method() == (mean, np, numpy.random, random)
