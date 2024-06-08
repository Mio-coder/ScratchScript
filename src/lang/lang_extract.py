"""
types:
program -> list[resource | code]
resource -> Node('resource', res_type: str, name: str contents: fields | code, init_value: expr)
code -> list[
    statement
    | fn_call
    | assign
    | event_stmt
]
assign -> Node(name: str, value: expr)
fn_call -> Node(
    name: attr
    args: list[expr]
)
attr -> list[str]
expr -> fn_call
    | attr
    | value
    | Node('expr', left: expr | None, op: str, right: op)

fields -> dict[str, value]
value -> str
    | int
    | float
    | Node('color', value: str)
    | tuple[float, float]

Resource types:
Sprite - curl code
Costume - fields
Sound - fields
Broadcast - none
Monitor - fields
Comment? - fields
Var - value
"""
from dataclasses import dataclass
from typing import Optional
from warnings import warn

from src.lang.lang_types import Resource, Code as ParserCode, Event, FnCall


class CompilerError(ValueError):
    pass


# class Code:
#     pass


@dataclass
class Costume:
    name: str


@dataclass
class Sound:
    name: str


@dataclass
class Variable:
    name: str


class Sprite:
    def __init__(self, name):
        self.name = name
        self.main_code = []
        self.code: dict[FnCall, list[ParserCode]] = dict()
        self.costumes = {}
        self.sounds = {}
        self.vars = {}

    def add_main_code(self, code):
        self.main_code.append(code)

    def add_event_code(self, event: FnCall, code: list[ParserCode]):
        if event in self.code:
            self.code[event] += code
        else:
            self.code[event] = code

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


def create_resource(v: Resource):
    return Sound("test")


def create_sprite(v: Resource, sprite: Optional[Sprite] = None):
    if isinstance(v.contents, dict):
        raise CompilerError("sprite requires code, consider changing () to {}")
    if v.init_value is not None:
        raise CompilerError("sprite does not accept default value")
    if v.contents is None:
        raise CompilerError("sprite requires code, no code specified")
    if sprite is None:
        sprite = Sprite(v.name)
    else:
        assert sprite.name == v.name
    for stmt in v.contents:
        if isinstance(stmt, Resource):
            sprite.add_resource(create_resource(stmt))
        elif isinstance(stmt, Event):
            sprite.add_event_code(stmt.name, stmt.code)
        elif isinstance(stmt, ParserCode):
            sprite.add_main_code(stmt)


def parse_program(n: list[ParserCode]):
    stage = StageSprite()
    sprites = {
        "Stage": stage
    }
    for v in n:
        if isinstance(v, Resource):
            if v.res_type != "sprite":
                raise CompilerError(f"only sprites and code are allowed as top-level, not {v.res_type}")
            if v.name.lower() in sprites:
                create_sprite(v, sprites[v.name.lower()])
            else:
                sprites[v.name] = create_sprite(v)
        elif isinstance(v, Event):
            stage.add_event_code(v.name, v.code)
        elif isinstance(v, ParserCode):
            stage.add_main_code(v)
        else:
            raise CompilerError(f"only sprites and code are allowed as top-level, not {type(v)}")
