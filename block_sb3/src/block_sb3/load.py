from pprint import pp

from msgspec import Struct
from msgspec.json import decode

from block_sb3.extract_types import Function, Field, Input, PrimitiveFunction


class Block(Struct):
    opcode: str
    inputs: dict[str, list]
    fields: dict[str, list]


class Target(Struct):
    blocks: dict[str, Block | list]


class Sb3File(Struct):
    targets: list[Target]


def load(data):
    ret = decode(data, type=Sb3File)
    ret: Sb3File
    blocks: dict[str, Block] = {}
    for target in ret.targets:
        blocks.update(target.blocks)
    id2fn: dict[str, PrimitiveFunction | Function] = {}
    functions: dict[str, PrimitiveFunction | Function] = {}
    update_inputs = []
    for block_id, block in blocks.items():
        if isinstance(block, list):
            if len(block) > 3:  # contains id
                fn = PrimitiveFunction(
                    block[0],
                    block[1],
                )
                functions[fn.block_opcode] = id2fn[block[2]] = fn
            continue
        to_update = False
        inputs = {}
        for name, inp in block.inputs.items():
            if isinstance(inp[1], list):
                val = None
            else:
                val = inp[1]
                to_update = True
            inputs[name] = Input(
                name,
                val
            )

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
            if isinstance(fn, PrimitiveFunction):
                print(f"ERROR: found primitive and normal blocks wit the same opcodes: {block.opcode}")
                continue
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
                inputs,
                fields
            )
        if to_update:
            update_inputs.append(fn)

    for to_update_fn in update_inputs:
        for name, inp in to_update_fn.inputs.items():
            if inp.block_opcode is not None and inp.block_opcode in id2fn:
                inp.block_opcode = id2fn[inp.block_opcode].opcode

        for name, field in to_update_fn.fields.items():
            new_functions = set()
            for functions_id in field.functions:
                new_functions.add(id2fn[functions_id])
            field.functions = new_functions
    return functions


if __name__ == '__main__':
    pp(load("move_functions.json"))
