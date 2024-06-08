from enum import IntEnum
from pprint import pp

from msgspec import Struct
from msgspec.json import decode


class Block(Struct):
    opcode: str
    inputs: dict[str, list]
    fields: dict[str, list]


class Target(Struct):
    blocks: dict[str, Block]


class Sb3File(Struct):
    targets: list[Target]


class Field(Struct):
    name: str
    possible_values: set
    functions: set["Function"] = set()


class Function(Struct):
    opcode: str
    inputs: list[str]
    fields: dict[str, Field]

    def __hash__(self):
        return hash((self.opcode, *self.inputs, *self.fields.keys()))


def main():
    file = "move_functions.json"
    with open(file) as f:
        ret = decode(f.read(), type=Sb3File)
    ret: Sb3File
    blocks: dict[str, Block] = {}
    for target in ret.targets:
        blocks.update(target.blocks)
    id2fn = {}
    functions: dict[str, Function] = {}
    update_inputs = []
    for block_id, block in blocks.items():
        to_update = False
        fields = {}
        for name, inp in block.fields.items():
            fields[name] = Field(
                name,
                {inp[0]}
            )
            if len(inp) == 2 and inp[1] is not None:
                fields[name].functions = {inp[1]}
                to_update = True
        if block.opcode in functions:
            fn = functions[block.opcode]
            for name, field in fn.fields.items():
                if name in fields:
                    field.possible_values.update(
                        fields[name].possible_values
                    )
                    field.functions.update(
                        fields[name].functions
                    )
                else:
                    print(f"WARN: field {name} not found in fields {fields} of {block.opcode}")
        else:
            fn = id2fn[block_id] = functions[block.opcode] = Function(
                block.opcode,
                list(block.inputs),
                fields
            )
        if to_update:
            update_inputs.append(fn)
    for to_update_fn in update_inputs:
        for name, field in to_update_fn.fields.items():
            new_functions = set()
            for functions_id in field.functions:
                new_functions.add(id2fn[functions_id])
            field.functions = new_functions
    pp(functions)


if __name__ == '__main__':
    main()
