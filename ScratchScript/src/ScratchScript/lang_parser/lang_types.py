from msgspec import Struct


class Expr:
    pass


class Code:
    pass


class MathExpr(Expr, Struct):
    left: "None | expr"
    op: str
    right: "expr"


class Color(Struct):
    value: str


class Angle(Struct):
    value: int


value = Angle | Color | str | int | float | tuple[float, float]

expr = Expr | list[str]


class Assignment(Code, Struct):
    name: str
    value: expr | value


class FnCallArgs(Struct):
    args: list[expr | value]
    kwargs: dict[str, expr | value]


class FnCall(Expr, Code, Struct):
    name: list[str]
    args: FnCallArgs


class Resource(Code, Struct):
    res_type: str
    name: str
    contents: list[Code] | dict[str, value] | None
    init_value: expr


class Event(Code, Struct):
    name: FnCall
    code: list[Code]
