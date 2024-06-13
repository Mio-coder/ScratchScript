from typing import Optional, Any

from msgspec import Struct
from msgspec.json import decode

from ScratchScript.lang_compiler.lang_function import FnSpec, get_raw_fn
from ScratchScript.lang_compiler.lang_types import StageSprite, Sprite, Variable, MAIN_CODE_EVENT
from ScratchScript.lang_parser.lang_types import Code, Assignment, FnCall, Expr

# FnCall(name=['motion', 'goto'], args=[100, 100])
data_setvariableto = get_raw_fn(decode("""
{
  "opcode": "data_setvariableto",
  "inputs": {
    "VALUE": {
      "name": "VALUE",
      "block_opcode": null
    }
  },
  "fields": {
    "VARIABLE": {
      "name": "VARIABLE",
      "possible_values": [
        "[variable]"
      ],
      "functions": [
        {
          "fn_type": 12,
          "name": "[variable]"
        }
      ]
    }
  }
}
""", type=FnSpec))


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


def parse_expr(expr: Expr) -> tuple[list, list, Any]:
    return [], [], 10


def parse_code(sprite: Sprite, stage: StageSprite):
    stage_state = State(stage.vars)
    sprite_state = State(sprite.vars, stage_state)
    code = sprite.code.copy()
    if sprite.main_code is not []:
        code[MAIN_CODE_EVENT] += sprite.main_code
    result = {}
    for name, code_block in code:
        result[name] = parse_code_block(code_block, sprite_state)

    return result


def parse_fn_call(fn_call: FnCall):
    pre = []
    post = []
    args = []
    for arg in fn_call.args:
        expr_pre, expr_post, expr = parse_expr(arg)
        pre += expr_pre
        expr_post += expr_post
        args += expr
    return []


def parse_code_block(code: list[Code], state: State):
    parsed_code = []
    for code_stmt in code:
        if isinstance(code_stmt, Assignment):
            pre, post, value = parse_expr(code_stmt.value)
            fn = data_setvariableto(
                inputs={
                    "VALUE": value
                },
                fields={
                    "VARIABLE": state.get(code_stmt.name)
                }
            )
            parsed_code += pre + [fn] + post
        elif isinstance(code_stmt, FnCall):
            parsed_code += parse_fn_call(code_stmt)
    return code
