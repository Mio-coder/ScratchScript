from msgspec import Struct


class Field(Struct):
    name: str
    possible_values: set
    functions: set["Function"] = set()


class Function(Struct):
    opcode: str
    inputs: list[str]
    fields: dict[str, Field]

    def __hash__(self):
        return hash((self.opcode, len(self.inputs), *self.inputs, len(self.fields), *self.fields.values()))
