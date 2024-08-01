from typing import Optional, Any

from msgspec import Struct

from PyScratch.PyScratch import Block
from ScratchScript.ScratchScript.lang_compiler.lang_function import get_function, FnBase
from ScratchScript.ScratchScript.lang_compiler.lang_types import StageSprite, Sprite, Variable
from ScratchScript.ScratchScript.lang_parser.lang_types import Code, Assignment, FnCall, Expr, FnCallArgs
from ScratchScript.ScratchScript.lang_compiler import setvariableto

# FnCall(name=['motion', 'goto'], args=[100, 100])


class State(Struct):
    variables: dict[str, Variable]
    parent: Optional["State"] = None

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise KeyError(f"Unknown variable {name}")


class GlobalState(Struct):
    sprites: dict[str, Sprite]

    @property
    def stage(self):
        return self.sprites["stage"]


# TODO: implement
def parse_expr(expr: Expr) -> Any:
    return 10


def parse_code(sprite: Sprite, stage: StageSprite):
    stage_state = State(stage.vars)
    sprite_state = State(sprite.vars, stage_state)
    code = sprite.code.copy()
    result = {}
    for name, code_block in code:
        result[name] = parse_code_block(code_block, sprite_state, parse_fn_call(name, sprite_state))
    return result


def parse_fn_call(fn_call: FnCall, state) -> FnBase:
    fn = get_function(fn_call.name)
    return fn(fn_call.args, state)


def parse_code_block(code: list[Code], state: State, root: FnBase) -> list[Block]:
    functions = [root]
    for code_stmt in code:
        if isinstance(code_stmt, Assignment):
            value = parse_expr(code_stmt.value)
            fn = setvariableto(FnCallArgs([value, code_stmt]), state)
        elif isinstance(code_stmt, FnCall):
            fn = parse_fn_call(code_stmt, state)
        else:
            continue
        functions.append(fn)
    parsed_code = []
    code: FnBase
    for previous_code, code, next_code in zip(
        [None] + functions[:-1],
        functions,
        functions[1:] + [None]
    ):
        parsed_code += code.get_blocks(next_code, previous_code)
    return parsed_code
