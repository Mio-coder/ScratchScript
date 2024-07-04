from collections import defaultdict
from warnings import warn

from msgspec import Struct

from ScratchScript.lang_parser.lang_types import Code, FnCall


class Costume(Struct):
    name: str


class Sound(Struct):
    name: str


class Variable(Struct):
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


class Program(Struct):
    sprites: dict[str, Sprite]

