import json
import subprocess
import sys

from typing import List, Optional, Set


class _ExtractedCode:
    def __init__(self, get_requirements: bool = True) -> None:
        self.name: str = ""
        self.code: str = ""
        self.dependencies: Set[str] = set()
        self.imports: Set[str] = set()
        self.requirements: Set[str] = set()
        if get_requirements:
            req = (
                subprocess.run(
                    [sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE
                )
                .stdout.decode(encoding="utf-8")
                .splitlines(keepends=False)
            )
            self.requirements = set(req)
        self.frozen_code: Optional[str] = None

    @staticmethod
    def from_string(string: str) -> "_ExtractedCode":
        json_dict = json.loads(string)
        assert isinstance(json_dict, dict)
        ret = _ExtractedCode(get_requirements=False)
        if "frozen_code" in json_dict.keys():
            ret.frozen_code = json_dict["frozen_code"]
        try:
            ret.name = json_dict["name"]
            ret.code = json_dict["code"]
            ret.dependencies = set(json_dict["dependencies"])
            ret.imports = set(json_dict["imports"])
            ret.requirements = set(json_dict["requirements"])
        except AttributeError:
            raise ValueError("Invalid code string")
        return ret

    def to_string(self, freeze_code: bool = True) -> str:
        dictionary = {
            "name": self.name,
            "code": self.code,
            "dependencies": list(self.dependencies),
            "imports": list(self.imports),
            "requirements": list(self.requirements),
        }
        if freeze_code:
            if self.frozen_code is None:
                self.frozen_code = self.to_code()
            dictionary["frozen_code"] = self.frozen_code
        return json.dumps(dictionary)

    def to_code(self) -> str:
        if self.frozen_code is not None:
            return self.frozen_code
        code = ""
        for imp in self.imports:
            code += imp + "\n"
        deps = []
        to_order = self.dependencies.copy()
        while len(to_order) > 0:
            for remaining_dep in to_order:
                tmp_deps = deps + [remaining_dep]
                if _test_dep_order(code, tmp_deps):
                    deps = tmp_deps
                    to_order.remove(remaining_dep)
                    break
        if len(deps) != len(self.dependencies):
            raise RuntimeError(
                f"Cannot find dependency order with dependencies {self.dependencies}"
            )
        for dep in deps:
            code += dep + "\n"
        code += self.code
        return code

    def __str__(self) -> str:
        if self.frozen_code is not None:
            ret = "----frozen code----\n" + self.frozen_code
        else:
            ret = "----name----\n"
            ret += self.name
            ret += "----code----\n"
            ret += self.code
            ret += "----imports----"
            for i in self.imports:
                ret += "\n" + i
            ret += "\n----dependencies----"
            for dep in self.dependencies:
                ret += "\n" + dep
        ret += (
            "\n----requirements----"
            if len(self.dependencies) == 0
            else "----requirements----"
        )
        for req in self.requirements:
            ret += "\n" + req
        return ret

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _ExtractedCode):
            return False
        return (
            other.name == self.name
            and other.code == self.code
            and other.dependencies == self.dependencies
            and other.imports == self.imports
            and other.requirements == self.requirements
            and other.frozen_code == self.frozen_code
        )


def _test_dep_order(code: str, deps: List[str]) -> bool:
    tmp_code = code
    for dep in deps:
        tmp_code += dep + "\n"
    try:
        exec(tmp_code, {})
    except NameError:
        return False
    return True
