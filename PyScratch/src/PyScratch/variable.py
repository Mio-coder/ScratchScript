from dataclasses import dataclass
from typing import Optional

from .primitives import PrimitiveBlock
from .utils import AutoId


@dataclass
class Variable(AutoId):
    name: str
    value: str
    is_cloud: bool

    def get(self):
        return [self.name, self.value, self.is_cloud]


@dataclass
class VariableBlock(AutoId, PrimitiveBlock):
    var: Variable
    x: Optional[int] = None  # if top level
    y: Optional[int] = None  # if top level

    def as_list(self):
        result = [12, self.var.name, self.item_id]
        if self.x is not None or self.y is not None:
            result += [self.x or 0, self.y or 0]
        return result


@dataclass
class ListVariable(AutoId):
    name: str
    values: list[str]

    def get(self):
        return [self.name, self.values]


@dataclass
class ListBlock(AutoId):
    var: ListVariable
    x: Optional[int] = None  # if top level
    y: Optional[int] = None  # if top level

    def as_list(self):
        result = [13, self.var.name, self.item_id]
        if self.x is not None or self.y is not None:
            result += [self.x or 0, self.y or 0]
        return result
