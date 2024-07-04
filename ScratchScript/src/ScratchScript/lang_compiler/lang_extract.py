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
from pprint import pp
from typing import Optional

from ScratchScript.lang_compiler.lang_types import Variable, Sprite, StageSprite, Program
from ScratchScript.lang_parser.lang_types import Assignment
from ScratchScript.lang_parser.lang_types import Resource, Code, Event


class CompilerError(ValueError):
    pass


def create_resource(v: Resource):
    if v.res_type == "sprite":
        return create_sprite(v)
    elif v.res_type == "var":
        return Variable(v.name)


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
        elif isinstance(stmt, Code):
            sprite.add_main_code(stmt)
            pp(stmt)


def parse_program(n: list[Code]):
    stage = StageSprite()
    sprites = {
        "Stage": stage
    }
    for v in n:
        if isinstance(v, Resource):
            if v.res_type == "sprite":
                if v.name.lower() in sprites:
                    create_sprite(v, sprites[v.name.lower()])
                else:
                    sprites[v.name] = create_sprite(v)
            elif v.res_type == "var":
                stage.add_resource(create_resource(v))
                if v.init_value is not None:
                    stage.add_main_code(Assignment(v.name, v.init_value))
            else:
                raise CompilerError(f"only sprites and code are allowed as top-level, not {v.res_type}")
        elif isinstance(v, Event):
            stage.add_event_code(v.name, v.code)
        elif isinstance(v, Code):
            stage.add_main_code(v)
        else:
            raise CompilerError(f"only sprites and code are allowed as top-level, not {type(v)}")
    program = Program(sprites)
    return program
