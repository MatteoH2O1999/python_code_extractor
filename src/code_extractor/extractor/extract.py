import importlib
import inspect
import itertools
import site
import sys

from types import ModuleType
from typing import Callable, Tuple, Type, Set, Union

from ..extracted_code import ExtractedCode


_ADDITIONAL_PATH_KEYWORDS: Set[str] = {"site-packages", "lib-dynload"}
_POSSIBLE_SITE_PATHS: Set[str] = {
    site.getuserbase(),
    site.getusersitepackages(),
    *site.getsitepackages(),
}
for sys_path in sys.path:
    for keyword in _ADDITIONAL_PATH_KEYWORDS:
        if keyword in sys_path:
            _POSSIBLE_SITE_PATHS.add(sys_path)


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
        pass
    for name, closure_var in global_closure_vars.items():
        if inspect.ismodule(closure_var):
            module_path = getattr(closure_var, "__file__", None)
            if module_path is not None:
                user_defined = True
                for possible_path in _POSSIBLE_SITE_PATHS:
                    if possible_path in module_path:
                        user_defined = False
            else:
                user_defined = False
            if user_defined:
                raise NotImplementedError(
                    f"Error with dependency {closure_var}: "
                    f"Not found in possible paths: {_POSSIBLE_SITE_PATHS}"
                    f"Package cannot extract user defined module dependencies yet"
                )
            else:
                imports.add(f"import {closure_var.__name__} as {name}")
                permutations = []
                for i in range(1, len(unbound_closure_vars) + 1):
                    for perm in itertools.permutations(unbound_closure_vars, i):
                        permutations.append(list(perm))
                for permutation in permutations:
                    possible_module = closure_var.__name__
                    for submodule in permutation:
                        possible_module += f".{submodule}"
                    try:
                        imported_submodule = importlib.import_module(possible_module)
                        assert inspect.ismodule(imported_submodule)
                        imports.add(f"import {possible_module} as {possible_module}")
                    except ModuleNotFoundError:
                        pass
        elif inspect.isroutine(closure_var):
            module = inspect.getmodule(closure_var)
            if module is None:
                module = _guess_module(closure_var)
            module_path = getattr(module, "__file__", None)
            if module_path is not None:
                user_defined = True
                for possible_path in _POSSIBLE_SITE_PATHS:
                    if possible_path in module_path:
                        user_defined = False
            else:
                user_defined = False
            if user_defined:
                if inspect.isbuiltin(closure_var):
                    raise ValueError(
                        f"Cannot save user-defined built-in function {closure_var}"
                    )
                else:
                    dependencies.add(inspect.getsource(closure_var))
                    new_dep, new_imp = _get_function_dependencies(closure_var)
                    dependencies.update(new_dep)
                    imports.update(new_imp)
            else:
                imports.add(
                    f"from {module.__name__} import {closure_var.__name__} as {name}"
                )
    for name, closure_var in non_local_closure_vars.items():
        pass
    for name in unbound_closure_vars:
        pass
    return dependencies, imports


def _guess_module(obj: Callable[..., object]) -> ModuleType:
    if inspect.isbuiltin(obj):
        instance = getattr(obj, "__self__", None)
        if instance is None:
            raise RuntimeError(f"Cannot identify module for {obj}")
        cls = getattr(instance, "__class__", None)
        if cls is None:
            raise RuntimeError(f"Cannot identify module for {obj}")
        module = inspect.getmodule(cls)
        if module is None:
            raise RuntimeError(f"Cannot identify module for {obj}")
        return module
    raise NotImplementedError(f"Cannot identify module for {obj}")
