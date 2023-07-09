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

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import _ExtractedCode
from code_extractor.extractor.extract import _POSSIBLE_SITE_PATHS

from dummy import DummyEnum, DummyEnumModule

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
_POSSIBLE_SITE_PATHS.add(os.path.join(CURRENT_DIRECTORY, "dummy"))


def function_enum():
    return DummyEnum.Dummy2


def function_enum_module():
    return DummyEnumModule.Dummy1


def test_extract_enum_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_enum.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(function_enum))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_enum_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_enum.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_enum"
    assert extracted_method().value == DummyEnum.Dummy2.value
    assert extracted_method().name == DummyEnum.Dummy2.name


def test_extract_module_enum_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_enum_module.json")
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(function_enum_module))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_module_enum_function():
    with open(
        os.path.join(CURRENT_DIRECTORY, "expected_results", "function_enum_module.json")
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_enum_module"
    assert extracted_method().value == DummyEnumModule.Dummy1.value
    assert extracted_method().name == DummyEnumModule.Dummy1.name
