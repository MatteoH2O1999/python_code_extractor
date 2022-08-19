"""
Module containing code for extracting source code from live python objects.
"""
import importlib
import inspect
import pickle
import os
import re
import site
import sys
import textwrap

from threading import Lock
from types import ModuleType
from typing import Callable, Dict, Iterable, Pattern, Tuple, Type, Set, Union
from warnings import warn

from ..extracted_code import _ExtractedCode

_MODULE_LOCK: Lock = Lock()
_SAVED_CODE: Set[str] = set()
_BUILTINS_MODULE_NAMES: Set[str] = {"__builtin__", "__builtins__", "builtins"}
_NESTED_DETECTOR: Pattern[str] = re.compile(
    r"(\A|\n)[\t ]+(async def |def )[a-zA-Z_-]+\([a-zA-Z0-9,:_.-\[\] ]*\)"
)
_ADDITIONAL_PATH_KEYWORDS: Set[str] = {os.path.dirname(os.__file__)}
_POSSIBLE_SITE_PATHS: Set[str] = {
    site.getuserbase(),
    site.getusersitepackages(),
    *site.getsitepackages(),
}
for sys_path in sys.path:
    for keyword in _ADDITIONAL_PATH_KEYWORDS:
        if keyword in sys_path:
            _POSSIBLE_SITE_PATHS.add(sys_path)


def extract_code(
    obj: Union[object, Type[object], Callable[..., object]],
    get_requirements: bool = False,
    freeze_code: bool = True,
) -> str:
    """
    Extract the source code from the specified object. If it is an instance, the code for the class is
    extracted, if it is a function, the code for the function is extracted. Dependencies and imports are
    extracted as well as imports (third-party dependencies) or source code (user-defined dependencies).

    :param obj: The object to extract the source code from.
    :type obj: type(object), Callable[..., object]
    :param get_requirements: If True will include a pip freeze in the string.
        Useful to ensure the environment is compatible.
    :type get_requirements: bool
    :param freeze_code: If True the code to recreate obj is calculated and included in the
        string.
    :type freeze_code: bool
    :return: The string with the extracted information.
    :rtype: str
    """
    if inspect.isbuiltin(obj):
        raise ValueError("Cannot extract code from builtins.")
    if inspect.isroutine(obj):
        if inspect.ismethod(obj):
            obj = obj.__getattribute__("__func__")
    elif not inspect.isclass(obj):
        obj = obj.__class__
    global _MODULE_LOCK
    global _SAVED_CODE
    with _MODULE_LOCK:
        to_return = _extract_code(obj, get_requirements=get_requirements).to_string(
            freeze_code=freeze_code
        )
        _SAVED_CODE = set()
    return to_return


def _extract_code(
    obj: Union[Type[object], Callable[..., object]], get_requirements: bool = False
) -> _ExtractedCode:
    extracted_code = _ExtractedCode(get_requirements=get_requirements)
    object_name = getattr(obj, "__name__", None)
    if object_name is None:
        raise RuntimeError(f"Expected {obj} to have attribute __name__")
    extracted_code.name = object_name
    source_code = textwrap.dedent(inspect.getsource(obj))
    _SAVED_CODE.add(source_code)
    if inspect.isroutine(obj):
        if source_code.startswith("@") and "@staticmethod\n" in source_code:
            source_code = source_code.replace("@staticmethod\n", "")
        if source_code.startswith("@") and "@property\n" in source_code:
            source_code = source_code.replace("@property\n", "")
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
                if closure_var.__name__ == name:
                    imports.add(f"import {closure_var.__name__}")
                else:
                    assert "." not in name
                    imports.add(f"import {closure_var.__name__} as {name}")
                possible_other_vars = list(unbound_closure_vars)
                possible_other_vars.extend(global_closure_vars.keys())
                modules = [closure_var.__name__]
                for module in modules:
                    for possible_other_var in possible_other_vars:
                        possible_module = f"{module}.{possible_other_var}"
                        try:
                            imported_submodule = importlib.import_module(
                                possible_module
                            )
                            assert inspect.ismodule(imported_submodule)
                            imports.add(f"import {possible_module}")
                            modules.append(possible_module)
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
                    if _has_source(closure_var):
                        if (
                            textwrap.dedent(inspect.getsource(closure_var))
                            not in _SAVED_CODE
                        ):
                            dependencies.add(
                                textwrap.dedent(inspect.getsource(closure_var))
                            )
                            _SAVED_CODE.add(
                                textwrap.dedent(inspect.getsource(closure_var))
                            )
                            new_dep, new_imp = _get_dependencies(closure_var)
                            dependencies.update(new_dep)
                            imports.update(new_imp)
                            if inspect.isclass(closure_var):
                                for parent in inspect.getmro(closure_var):
                                    if parent.__module__ not in _BUILTINS_MODULE_NAMES:
                                        source = textwrap.dedent(
                                            inspect.getsource(parent)
                                        )
                                        if (
                                            source not in dependencies
                                            and source not in _SAVED_CODE
                                        ):
                                            dependencies.add(source)
                                            _SAVED_CODE.add(source)
                                            new_dep, new_imp = _get_dependencies(parent)
                                            dependencies.update(new_dep)
                                            imports.update(new_imp)
                    else:
                        new_dep, new_imp = _pickle(name, closure_var)
                        dependencies.update(new_dep)
                        imports.update(new_imp)
            else:
                if closure_var.__name__ == name:
                    imports.add(f"from {module.__name__} import {closure_var.__name__}")
                else:
                    assert "." not in name
                    imports.add(
                        f"from {module.__name__} import {closure_var.__name__} as {name}"
                    )
        else:
            new_dep, new_imp = _pickle(name, closure_var)
            dependencies.update(new_dep)
            imports.update(new_imp)
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


def _has_source(obj: Union[Type[object], Callable[..., object]]) -> bool:
    try:
        inspect.getsource(obj)
    except OSError:
        return False
    return True


def _pickle(name: str, closure_var: object) -> Tuple[Set[str], Set[str]]:
    imports = set()
    dependencies = set()
    warn(
        f"Variable {name} with content {closure_var} cannot be safely saved. "
        f"Will fallback to pickle the value but compatibility with different versions "
        f"is not guaranteed."
    )
    try:
        bytes_string = pickle.dumps(closure_var, protocol=4, fix_imports=False)
    except pickle.PicklingError:
        raise RuntimeError(
            f"Cannot pickle dependency {name} with content {closure_var}."
        )
    test_reconstruct = pickle.loads(bytes_string)
    equality: Union[bool, Iterable[bool]] = test_reconstruct == closure_var
    if isinstance(equality, Iterable):
        equality = all(equality)
    else:
        assert isinstance(equality, bool)
    if not equality:
        raise RuntimeError(
            f"Cannot reconstruct object {name} with content {closure_var} from pickling."
        )
    imports.add("import pickle")
    dependencies.add(f"{name} = pickle.loads({bytes_string})")
    return dependencies, imports
