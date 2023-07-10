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
Module containing code to save values as literals
"""
import enum
import pickle

from typing import Tuple, Set, Type, Dict, List


_BUILTINS_TYPES: Set[Type[object]] = {
    bool,
    int,
    float,
    list,
    tuple,
    dict,
    complex,
    range,
    str,
    bytes,
    bytearray,
    memoryview,
    set,
    frozenset,
}


def _save_literal(name: str, closure_var: object) -> Tuple[Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    if isinstance(closure_var, dict):
        value, new_dep, new_imp = _save_dict(closure_var)
        imports.update(new_imp)
        dependencies.update(new_dep)
        dependencies.add(f"{name} = {value}\n")
    elif isinstance(closure_var, list):
        value, new_dep, new_imp = _save_list(closure_var)
        imports.update(new_imp)
        dependencies.update(new_dep)
        dependencies.add(f"{name} = {value}\n")
    elif isinstance(closure_var, set):
        value, new_dep, new_imp = _save_set(closure_var)
        imports.update(new_imp)
        dependencies.update(new_dep)
        dependencies.add(f"{name} = {value}\n")
    elif isinstance(closure_var, tuple):
        value, new_dep, new_imp = _save_tuple(closure_var)
        imports.update(new_imp)
        dependencies.update(new_dep)
        dependencies.add(f"{name} = {value}\n")
    else:
        closure_var, new_dep, new_imp = _save_value(closure_var)
        imports.update(new_imp)
        dependencies.update(new_dep)
        dependencies.add(f"{name} = {closure_var}\n")
    return dependencies, imports


def _save_list(li: List[object]) -> Tuple[str, Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    to_write = "["
    for element in li:
        element, new_dep, new_imp = _save_value(element)
        imports.update(new_imp)
        dependencies.update(new_dep)
        to_write += f"{element}, "
    if to_write.endswith(", "):
        to_write = to_write[:-2]
    to_write += "]"
    return to_write, dependencies, imports


def _save_tuple(t: Tuple[object, ...]) -> Tuple[str, Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    to_write = "("
    for element in t:
        element, new_dep, new_imp = _save_value(element)
        imports.update(new_imp)
        dependencies.update(new_dep)
        to_write += f"{element}, "
    if to_write.endswith(", "):
        to_write = to_write[:-2]
    to_write += ")"
    return to_write, dependencies, imports


def _save_set(s: Set[object]) -> Tuple[str, Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    to_write = "{"
    for element in s:
        element, new_dep, new_imp = _save_value(element)
        imports.update(new_imp)
        dependencies.update(new_dep)
        to_write += f"{element}, "
    if to_write.endswith(", "):
        to_write = to_write[:-2]
    to_write += "}"
    return to_write, dependencies, imports


def _save_dict(d: Dict[object, object]) -> Tuple[str, Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    to_write = "{"
    for key, value in d.items():
        key, new_dep, new_imp = _save_value(key)
        imports.update(new_imp)
        dependencies.update(new_dep)
        value, new_dep, new_imp = _save_value(value)
        imports.update(new_imp)
        dependencies.update(new_dep)
        to_write += f"{key}: {value}, "
    if to_write.endswith(", "):
        to_write = to_write[:-2]
    to_write += "}"
    return to_write, dependencies, imports


def _save_value(obj: object) -> Tuple[str, Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    if isinstance(obj, str):
        obj = f"'{obj}'"
    if isinstance(obj, enum.Enum):
        module = obj.__module__
        if module == "__main__":
            module = ""
        name = obj.__class__.__name__
        new_dep, new_imp = _save_enum(obj.__class__, module, name)
        imports.update(new_imp)
        dependencies.update(new_dep)
        if module:
            obj = f"{module}.{name}.{obj.name}"
        else:
            obj = f"{obj}"
    if type(obj) not in _BUILTINS_TYPES:
        imports.add("import pickle")
        obj = f"pickle.loads({pickle.dumps(obj)})"
    return str(obj), dependencies, imports


def _save_enum(e: enum.EnumMeta, module: str, name: str) -> Tuple[Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    imports.add("import enum")
    names = [(data.name, data.value) for data in e]
    if module:
        imports.add(f"import {module}")
        dependencies.add(
            f"{module}.{name} = enum.Enum(value='{name}', module='{module}', names={names})\n"
        )
    else:
        dependencies.add(f"{name} = enum.Enum(value='{name}', names={names})\n")
    return dependencies, imports
