# Python package to extract source code from live object.
# Copyright (C) 2022 Matteo Dell'Acqua
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import inspect
import os
import numpy as np
import numpy.random

from numpy import mean
from numpy.random import random

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import _ExtractedCode

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
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(function_11))
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
