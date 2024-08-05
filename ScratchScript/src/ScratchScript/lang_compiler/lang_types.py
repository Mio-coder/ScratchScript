from collections import defaultdict
from typing import Optional, TYPE_CHECKING
from warnings import warn

from msgspec import Struct

from PyScratch.variable import Variable
from ..lang_parser.lang_types import Code

if TYPE_CHECKING:
    from .lang_function import FnBase


class State(Struct):
    variables: dict[str, Variable]
    parent: Optional["State"] = None

    def get(self, name) -> Variable:
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise KeyError(f"Unknown variable {name}")


class GlobalState(Struct):
    sprites: dict[str, "Sprite"]

    @property
    def stage(self):
        return self.sprites["stage"]


class Costume(Struct):
    name: str


class Sound(Struct):
    name: str


class Variable(Struct):
    name: str

    def to_expr(self):
        return


class Sprite:
    def __init__(self, name: str, main_event: "FnBase"):
        self.name = name
        # noinspection PyTypeChecker
        self.code: dict[FnBase, list[list["FnBase"]]] = defaultdict(default_factory=list)
        self.code[main_event] = []
        self.main_code = self.code[main_event][0]
        self.costumes = {}
        self.sounds = {}
        self.vars = {}

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
    def __init__(self, main_event: "FnBase"):
        super().__init__("Stage", main_event)


class Program(Struct):
    sprites: dict[str, Sprite]
