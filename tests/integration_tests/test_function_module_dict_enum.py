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
import enum
import inspect
import os

from code_extractor import extract_code, load_code
from code_extractor.extracted_code import _ExtractedCode
from code_extractor.extractor.extract import _POSSIBLE_SITE_PATHS

import dummy

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
_POSSIBLE_SITE_PATHS.add(os.path.join(CURRENT_DIRECTORY, "dummy"))


def function_module_dict_enum():
    return dummy.dummy_dict_enum


def test_extract_module_dict_enum_function():
    with open(
        os.path.join(
            CURRENT_DIRECTORY, "expected_results", "function_module_dict_enum.json"
        )
    ) as json_file:
        json_txt = json_file.read()
    expected_code = _ExtractedCode.from_string(json_txt)
    extracted_code = _ExtractedCode.from_string(extract_code(function_module_dict_enum))
    assert extracted_code.name == expected_code.name
    assert extracted_code.code == expected_code.code
    assert extracted_code.dependencies == expected_code.dependencies
    assert extracted_code.imports == expected_code.imports


def test_load_module_dict_enum_function():
    with open(
        os.path.join(
            CURRENT_DIRECTORY, "expected_results", "function_module_dict_enum.json"
        )
    ) as json_file:
        json_txt = json_file.read()
    extracted_method = load_code(json_txt)
    assert inspect.isfunction(extracted_method)
    assert extracted_method.__name__ == "function_module_dict_enum"
    enum_eq(extracted_method(), dummy.dummy_dict_enum)


def enum_eq(d1, d2):
    assert len(d1) == len(d2)
    for item1, item2 in zip(d1.items(), d2.items()):
        key1, value1 = item1
        key2, value2 = item2
        if isinstance(key1, enum.Enum):
            assert key1.name == key2.name
            assert key1.value == key2.value
            assert value1 == value2
        else:
            assert key1 == key2
            assert value1 == value2
