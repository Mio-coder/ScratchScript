from typing import Optional

from msgspec import Struct


class Input(Struct):
    name: str
    block_opcode: Optional[str] = None


class Field(Struct):
    name: str
    possible_values: set
    functions: set["Function | str"] = set()


class Function(Struct):
    opcode: str
    inputs: dict[str, Input]
    fields: dict[str, Field]

    def __hash__(self):
        return hash((self.opcode, len(self.inputs), *self.inputs, len(self.fields), *self.fields.values()))


class PrimitiveFunction(Struct):
    fn_type: int
    name: str

    @property
    def block_opcode(self):
        return {
            11: "Broadcast",
            12: "data_variable",
            13: "data_variable",
        }[self.fn_type]

    def __hash__(self):
        return hash((self.fn_type, self.name))
