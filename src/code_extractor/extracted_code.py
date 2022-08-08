import json

from typing import Any, List


class ExtractedCode:
    def __init__(self) -> None:
        self.code: str = ""
        self.dependencies: List[str] = []

    @staticmethod
    def from_string(string: str) -> "ExtractedCode":
        json_dict = json.loads(string)
        ret = ExtractedCode()
        try:
            ret.code = json_dict["code"]
            ret.dependencies = json_dict["dependencies"]
        except AttributeError:
            raise ValueError("Invalid code string")
        return ret

    def to_string(self) -> str:
        dictionary = {"code": self.code, "dependencies": self.dependencies}
        return json.dumps(dictionary)

    def __str__(self) -> str:
        ret = "----code----\n"
        ret += self.code
        ret += "----dependencies----"
        for dep in self.dependencies:
            ret += "\n" + dep
        return ret

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtractedCode):
            return False
        return other.code == self.code and other.dependencies == self.dependencies
