import json

from typing import Set


class ExtractedCode:
    def __init__(self) -> None:
        self.name: str = ""
        self.code: str = ""
        self.dependencies: Set[str] = set()
        self.imports: Set[str] = set()

    @staticmethod
    def from_string(string: str) -> "ExtractedCode":
        json_dict = json.loads(string)
        ret = ExtractedCode()
        try:
            ret.name = json_dict["name"]
            ret.code = json_dict["code"]
            ret.dependencies = set(json_dict["dependencies"])
            ret.imports = set(json_dict["imports"])
        except AttributeError:
            raise ValueError("Invalid code string")
        return ret

    def to_string(self) -> str:
        dictionary = {
            "name": self.name,
            "code": self.code,
            "dependencies": list(self.dependencies),
            "imports": list(self.imports),
        }
        return json.dumps(dictionary)

    def __str__(self) -> str:
        ret = "----name----"
        ret += self.name
        ret += "----code----"
        ret += self.code
        ret += "----imports----"
        for i in self.imports:
            ret += "\n" + i
        ret += "----dependencies----"
        for dep in self.dependencies:
            ret += "\n" + dep
        return ret

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtractedCode):
            return False
        return (
            other.name == self.name
            and other.code == self.code
            and other.dependencies == self.dependencies
            and other.imports == self.imports
        )
