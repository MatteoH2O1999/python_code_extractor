import json
import subprocess
import sys

from typing import Set


class ExtractedCode:
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

    @staticmethod
    def from_string(string: str) -> "ExtractedCode":
        json_dict = json.loads(string)
        ret = ExtractedCode(get_requirements=False)
        try:
            ret.name = json_dict["name"]
            ret.code = json_dict["code"]
            ret.dependencies = set(json_dict["dependencies"])
            ret.imports = set(json_dict["imports"])
            ret.requirements = set(json_dict["requirements"])
        except AttributeError:
            raise ValueError("Invalid code string")
        return ret

    def to_string(self) -> str:
        dictionary = {
            "name": self.name,
            "code": self.code,
            "dependencies": list(self.dependencies),
            "imports": list(self.imports),
            "requirements": list(self.requirements),
        }
        return json.dumps(dictionary)

    def to_code(self) -> str:
        code = ""
        for imp in self.imports:
            code += imp + "\n"
        for dep in self.dependencies:
            code += dep + "\n"
        code += self.code
        return code

    def __str__(self) -> str:
        ret = "----name----"
        ret += self.name
        ret += "\n----code----"
        ret += self.code
        ret += "\n----imports----"
        for i in self.imports:
            ret += "\n" + i
        ret += "\n----dependencies----"
        for dep in self.dependencies:
            ret += "\n" + dep
        ret += "\n----requirements----"
        for req in self.requirements:
            ret += "\n" + req
        return ret

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtractedCode):
            return False
        return (
            other.name == self.name
            and other.code == self.code
            and other.dependencies == self.dependencies
            and other.imports == self.imports
            and other.requirements == self.requirements
        )
