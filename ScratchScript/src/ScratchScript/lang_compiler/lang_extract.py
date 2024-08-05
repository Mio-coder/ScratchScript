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
from typing import Optional

from .lang_code import parse_code_block
from .lang_function import parse_fn
from .lang_types import Variable, Sprite, StageSprite, Program, State
from ..lang_parser.lang_types import Assignment, Resource, Code, Event, FnCall, FnCallArgs


class CompilerError(ValueError):
    pass


def create_resource(v: Resource):
    if v.res_type == "sprite":
        return create_sprite(v)
    elif v.res_type == "var":
        return Variable(v.name)


MAIN_CODE_EVENT = FnCall(["whenflagclicked"], FnCallArgs([], dict()))


def create_sprite(v: Resource, stage_state: State, sprite: Optional[Sprite] = None):
    if isinstance(v.contents, dict):
        raise CompilerError("sprite requires code, consider changing () to {}")
    if v.init_value is not None:
        raise CompilerError("sprite does not accept default value")
    if v.contents is None:
        raise CompilerError("sprite requires code, no code specified")
    if sprite is None:
        sprite = Sprite(v.name, parse_fn(MAIN_CODE_EVENT))
    else:
        assert sprite.name == v.name
    sprite_state = State(sprite.vars, stage_state)
    main_code = []
    for stmt in v.contents:
        if isinstance(stmt, Resource):
            if v.res_type == "var":
                sprite.add_resource(create_resource(v))
            if v.init_value is not None:
                main_code.append(Assignment(v.name, v.init_value))
            else:
                sprite.add_resource(create_resource(stmt))
        elif isinstance(v, Event):
            event_fn = parse_fn(v.name)
            sprite.code[event_fn].append(parse_code_block(v.code, sprite_state, event_fn))
        elif isinstance(v, Code):
            main_code.append(v)


def parse_program(n: list[Code]):
    stage = StageSprite(parse_fn(MAIN_CODE_EVENT))
    sprites = {
        "Stage": stage
    }
    stage_state = State(stage.vars)
    main_code = []
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
                    main_code.append(Assignment(v.name, v.init_value))
                else:
                    raise CompilerError(f"only sprites and code are allowed as top-level, not {v.res_type}")
            elif isinstance(v, Event):
                event_fn = parse_fn(v.name)
                stage.code[event_fn].append(parse_code_block(v.code, stage_state, event_fn))
            elif isinstance(v, Code):
                main_code.append(v)
            else:
                raise CompilerError(f"only sprites and code are allowed as top-level, not {type(v)}")
    stage.main_code = parse_code_block(main_code, stage_state, parse_fn(MAIN_CODE_EVENT))
    program = Program(sprites)
    return program
