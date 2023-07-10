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
"""
Allows to save python functions and classes and load them without knowing the code.

This exports:
    - extract_code: to extract code to a string
    - load_code: to load code from a string extracted by this package
    - dump, dumps, load, loads: familiar API from the pickle and marshal modules
"""
__version__ = "0.4.1"

from .extractor.extract import extract_code
from .loader.load import load_code
from .pickle import dump, dumps, load, loads
