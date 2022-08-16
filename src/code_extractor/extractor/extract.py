import importlib
import inspect
import itertools
import site
import sys
import re
import textwrap

from types import ModuleType
from typing import Callable, Dict, Pattern, Tuple, Type, Set, Union

from ..extracted_code import ExtractedCode

_BUILTINS_MODULE_NAMES: Set[str] = {"__builtin__", "__builtins__", "builtins"}
_NESTED_DETECTOR: Pattern[str] = re.compile(
    r"(\A|\n)[\t ]+(async def |def )[a-zA-Z_-]+\([a-zA-Z0-9,:_.-\[\] ]*\)"
)
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
    if inspect.isbuiltin(obj):
        raise ValueError("Cannot extract code from builtins.")
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
    source_code = textwrap.dedent(inspect.getsource(obj))
    if inspect.isroutine(obj):
        if source_code.startswith("@") and "@staticmethod\n" in source_code:
            source_code = source_code.replace("@staticmethod\n", "")
    extracted_code.code = source_code
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
            if inspect.isfunction(func):
                new_dep, new_imp = _get_function_dependencies(func)
                dependencies.update(new_dep)
                imports.update(new_imp)
    return dependencies, imports


def _get_function_dependencies(obj: Callable[..., object]) -> Tuple[Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    closure_vars = inspect.getclosurevars(obj)
    builtins_closure_vars = closure_vars.builtins
    global_closure_vars = closure_vars.globals
    non_local_closure_vars = closure_vars.nonlocals
    unbound_closure_vars = closure_vars.unbound
    if _NESTED_DETECTOR.search(inspect.getsource(obj)) is not None:
        global_closure_vars = dict(global_closure_vars)
        global_closure_vars.update(_get_nested_globals(obj))
    print(closure_vars)
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
                possible_other_vars = list(unbound_closure_vars)
                possible_other_vars.extend(global_closure_vars)
                for i in range(1, len(possible_other_vars) + 1):
                    for perm in itertools.permutations(possible_other_vars, i):
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
        elif inspect.isroutine(closure_var) or inspect.isclass(closure_var):
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
                    dependencies.add(textwrap.dedent(inspect.getsource(closure_var)))
                    new_dep, new_imp = _get_dependencies(closure_var)
                    dependencies.update(new_dep)
                    imports.update(new_imp)
                    if inspect.isclass(closure_var):
                        for parent in inspect.getmro(closure_var):
                            if parent.__module__ not in _BUILTINS_MODULE_NAMES:
                                source = textwrap.dedent(inspect.getsource(parent))
                                if source not in dependencies:
                                    dependencies.add(source)
                                    new_dep, new_imp = _get_dependencies(parent)
                                    dependencies.update(new_dep)
                                    imports.update(new_imp)
            else:
                imports.add(
                    f"from {module.__name__} import {closure_var.__name__} as {name}"
                )
        else:
            raise RuntimeError(f"Cannot save dependency {closure_var}.")
    for name, closure_var in non_local_closure_vars.items():
        pass
    for name in unbound_closure_vars:
        pass
    return dependencies, imports


def _guess_module(obj: Union[Type[object], Callable[..., object]]) -> ModuleType:
    module = inspect.getmodule(obj)
    if module is not None:
        return module
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


def _get_nested_globals(obj: Callable[..., object]) -> Dict[str, object]:
    glob = {}
    obj_name = getattr(obj, "__name__", None)
    if obj_name is not None:
        source = inspect.getsource(obj)
        declared = vars(inspect.getmodule(obj))
        for name, o in declared.items():
            if name != obj_name and name in source:
                glob[name] = o
    return glob
