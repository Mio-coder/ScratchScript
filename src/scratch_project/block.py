from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from .broadcast import Broadcast
from .mutation import Mutation
from .primitives import PrimitiveBlock
from .utils import AutoId, from_dict
from .variable import ListVariable, Variable


def as_value(value: "Block | PrimitiveBlock"):
    if isinstance(value, Block):
        return value.item_id
    elif isinstance(value, PrimitiveBlock):
        return value.as_list()
    return value


class InputType(IntEnum):
    shadow = 1
    "input sname block shadow, unodscured shadow"
    no_shadow = 2
    "input block no shadow, no shadow"
    obscured_shadow = 3
    "input diff block no shadow, obscured shadow"


@dataclass
class BlockInput:
    name: str
    type: InputType
    value: "Block | PrimitiveBlock"
    obscured_by: Optional["Block | PrimitiveBlock"] = None

    def as_tuple(self):
        obscured_value = ([as_value(self.obscured_by)]
                          if self.obscured_by is not None else [])
        return (self.name,
                [self.type.value, as_value(self.value)] + obscured_value)


@dataclass
class BlockField:
    name: str
    value: str | Variable | ListVariable | Broadcast

    def as_tuple(self):
        value_id = [self.value.item_id] \
            if isinstance(self.value, AutoId) else []
        return (self.name, [self.value] + value_id)


@dataclass
class Block(AutoId, short_name="Block"):
    opcode: str
    inputs: list[BlockInput]  # d[name] = [type, id | inlineBlock] <= input
    fields: list[BlockField]  # d[name] = [value, (ID of value)?] <= field
    shadow: bool
    next_block: Optional["Block"] = None
    parent: Optional["Block"] = None
    # parent is None
    x: Optional[int] = None  # if top_level
    y: Optional[int] = None  # if top_level
    mutation: Optional[Mutation] = None
    """opcode == "procedures_call", "procedures_prototype", "control_stop" """

    def __post_init__(self):
        if self.mutation is not None:
            self.mutation.function = self
        return super().__post_init__()

    @property
    def top_level(self):
        return self.parent == None

    def as_tuple(self):
        result = {
            "opcode": self.opcode,
            "next": self.next_block,
            "parent": self.parent,
            "inputs": from_dict(self.inputs),
            "fields": from_dict(self.fields),
            "shadow": self.shadow,
            "topLevel": self.top_level
        }
        if self.top_level:
            result["x"] = self.x or 0
            result["y"] = self.y or 0
        if self.mutation is not None:
            result["mutation"] = self.mutation.as_dict()
        return (self.item_id, result)
