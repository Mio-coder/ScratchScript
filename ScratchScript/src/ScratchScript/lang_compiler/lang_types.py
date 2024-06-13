from collections import defaultdict
from dataclasses import dataclass
from warnings import warn

from ScratchScript.lang_parser.lang_types import Code, FnCall


@dataclass
class Costume:
    name: str


@dataclass
class Sound:
    name: str


@dataclass
class Variable:
    name: str


MAIN_CODE_EVENT = FnCall("event.test", [])


class Sprite:
    def __init__(self, name):
        self.name = name
        self.main_code = []
        # noinspection PyTypeChecker
        self.code: dict[FnCall, list[Code]] = defaultdict(default_factory=list)
        self.costumes = {}
        self.sounds = {}
        self.vars = {}

    def add_main_code(self, code):
        self.main_code.append(code)

    def add_event_code(self, event: FnCall, code: list[Code]):
        self.code[event] += code

    def add_resource(self, res):
        table = {
            Sound: self.sounds,
            Costume: self.costumes,
            Variable: self.vars
        }.get(res)
        if res.name in table:
            warn(f"redeclaration of resource {res}")
        table[res.name] = res


class StageSprite(Sprite):
    def __init__(self):
        super().__init__("Stage")
