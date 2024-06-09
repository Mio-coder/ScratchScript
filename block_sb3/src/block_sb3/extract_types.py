from typing import Optional

from msgspec import Struct


class Input(Struct):
    name: str
    block_opcode: Optional[str] = None


class Field(Struct):
    name: str
    possible_values: set
    functions: set["Function"] = set()


class Function(Struct):
    opcode: str
    inputs: dict[str, Input]
    fields: dict[str, Field]

    def __hash__(self):
        return hash((self.opcode, len(self.inputs), *self.inputs, len(self.fields), *self.fields.values()))
