from dataclasses import dataclass


class Expr:
    pass


class Code:
    pass


@dataclass
class MathExpr(Expr):
    left: "None | expr"
    op: str
    right: "expr"


@dataclass
class Color:
    value: str


value = Color | str | int | float | tuple[float, float]

expr = Expr | list[str]


@dataclass
class Assignment(Code):
    name: str
    value: expr | value


@dataclass
class FnCall(Expr, Code):
    name: list[str]
    args: list[expr | value]


@dataclass
class Resource(Code):
    res_type: str
    name: str
    contents: list[Code] | dict[str, value] | None
    init_value: expr


@dataclass
class Event(Code):
    name: FnCall
    code: list[Code]
