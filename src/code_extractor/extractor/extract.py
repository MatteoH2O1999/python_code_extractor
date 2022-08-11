import inspect
import itertools
from typing import Callable, Tuple, Type, Set, Union

from ..extracted_code import ExtractedCode


def extract_code(obj: Union[object, Type[object], Callable[..., object]]) -> str:
    if inspect.isroutine(obj):
        if inspect.ismethod(obj):
            obj = obj.__getattribute__("__func__")
    elif not inspect.isclass(obj):
        obj = obj.__class__
    return _extract_code(obj).to_string()


def _extract_code(obj: Union[Type[object], Callable[..., object]]) -> ExtractedCode:
    extracted_code = ExtractedCode()
    object_name = getattr(obj, "__name__", None)
    if object_name is None:
        raise RuntimeError(f"Expected {obj} to have attribute __name__")
    extracted_code.name = object_name
    extracted_code.code = inspect.getsource(obj)
    dependencies, imports = _get_dependencies(obj)
    extracted_code.dependencies = dependencies
    extracted_code.imports = imports
    return extracted_code


def _get_dependencies(
    obj: Union[Type[object], Callable[..., object]]
) -> Tuple[Set[str], Set[str]]:
    if inspect.isroutine(obj):
        dependencies, imports = _get_function_dependencies(obj)
    else:
        assert inspect.isclass(obj)
        imports = set()
        dependencies = set()
        functions = dir(obj)
        for function_name in functions:
            func = getattr(obj, function_name)
            if inspect.isroutine(func):
                new_dep, new_imp = _get_function_dependencies(func)
                dependencies.update(new_dep)
                imports.update(new_imp)
    return dependencies, imports


def _get_function_dependencies(obj: Callable[..., object]) -> Tuple[Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    closure_vars = inspect.getclosurevars(obj)
    print(closure_vars)
    builtins_closure_vars = closure_vars.builtins
    global_closure_vars = closure_vars.globals
    non_local_closure_vars = closure_vars.nonlocals
    unbound_closure_vars = closure_vars.unbound
    for name, closure_var in builtins_closure_vars.items():
        print(name, closure_var)
    for name, closure_var in global_closure_vars.items():
        if inspect.ismodule(closure_var):
            imports.add(f"import {closure_var.__name__} as {name}")
        permutations = []
        for i in range(1, len(unbound_closure_vars) + 1):
            for perm in itertools.permutations(unbound_closure_vars, i):
                permutations.append(list(perm))
    for name, closure_var in non_local_closure_vars.items():
        print(name, closure_var)
    for name in unbound_closure_vars:
        print(name)
    return dependencies, imports
