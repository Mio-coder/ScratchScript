from typing import Any

from PyScratch.block import Block, PrimitiveBlock
from PyScratch.primitives import Color as ColorBlock, String, Integer, Number,
from .lang_function import FnBase, parse_fn
from .lang_types import Sprite, State
from .modules.data import setvariableto
from ..lang_parser.lang_types import Code, Assignment, FnCall, FnCallArgs, expr as expr_type, Color


# TODO: implement
def parse_expr(expr: expr_type) -> PrimitiveBlock:
    if isinstance(expr, Color):
        return ColorBlock(expr.value)
    if isinstance(expr, str):
        return String(expr)
    if isinstance(expr, int):
        return Integer(expr)
    if isinstance(expr, float):
        return Number(expr)
    if isinstance(expr, tuple):
        # unsupported
        raise ValueError("unsupported")
    return 10


def parse_code_block(code: list[Code], state: State, root: FnBase) -> list[FnBase]:
    functions = [root]
    for code_stmt in code:
        if isinstance(code_stmt, Assignment):
            value = parse_expr(code_stmt.value)
            fn = setvariableto(FnCallArgs([value, code_stmt]), state)
        elif isinstance(code_stmt, FnCall):
            fn = parse_fn(code_stmt, state)
        else:
            continue
        functions.append(fn)
    return functions


"""
    parsed_code = []
    code: FnBase
    for previous_code, code, next_code in zip(
            [None] + functions[:-1],
            functions,
            functions[1:] + [None]
    ):
        parsed_code += code.get_blocks(next_code, previous_code)
"""
