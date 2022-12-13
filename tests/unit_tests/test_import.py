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

import code_extractor
import code_extractor.pickle as code_pickler


def test_import_module():
    assert getattr(code_extractor, "extract_code", None) is not None
    assert getattr(code_extractor, "load_code", None) is not None
    assert inspect.isfunction(code_extractor.extract_code)
    assert inspect.isfunction(code_extractor.load_code)


def test_import_pickle():
    assert getattr(code_pickler, "dumps", None) is not None
    assert getattr(code_pickler, "dump", None) is not None
    assert getattr(code_pickler, "loads", None) is not None
    assert getattr(code_pickler, "load", None) is not None
    assert inspect.isfunction(code_pickler.load)
    assert inspect.isfunction(code_pickler.loads)
    assert inspect.isfunction(code_pickler.dump)
    assert inspect.isfunction(code_pickler.dumps)
