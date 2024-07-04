from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Any

from msgspec import Struct
from msgspec.json import decode

from PyScratch.block import BlockInput, Block, InputType, BlockField
from PyScratch.primitives import PrimitiveBlock
from ScratchScript.lang_compiler.lang_types import Sprite, Variable


class FnInputSpec(Struct):
    name: str
    block_opcode: Optional[str] = None


class FnFieldsSpec(Struct):
    name: str
    possible_values: set
    functions: set["FnSpec"] = set()


class FnSpec(Struct):
    opcode: str
    inputs: dict[str, FnInputSpec]
    fields: dict[str, FnFieldsSpec]


specs_dir = Path(__file__).parent.parent / "function_specs"


def get_spec(spec_name) -> dict[str, FnSpec]:
    file = specs_dir / (spec_name + ".fnspec.json")
    with file.open() as f:
        return decode(f.read(), type=dict[str, FnSpec])


def as_primitive(value):
    return PrimitiveBlock()


class FnInput(Struct):
    name: str
    value: Any

    def as_block_input(self):
        value = self.value.block if isinstance(self.value, RawFnBase) else as_primitive(self.value)
        return BlockInput(self.name, InputType.no_shadow, value)


class FnFieldBase(Struct):
    name: str
    value: str | Sprite

    @abstractmethod
    def as_block_field(self):
        ...


def get_field(field_spec: FnFieldsSpec) -> type[FnFieldBase]:
    class FnField(FnFieldBase, Struct):
        def __post_init__(self):
            assert self.name == field_spec.name, "Names do not match"
            if isinstance(self.value, Sprite):
                if "[sprite]" not in list(map(str.lower, field_spec.possible_values)):
                    raise ValueError("Value is Sprite but sprite is not accepted as a value")
            elif isinstance(self.value, Variable):
                if "[variable]" not in list(map(str.lower, field_spec.possible_values)):
                    raise ValueError("Value is Variable but sprite is not accepted as a value")
            elif self.value not in field_spec.possible_values:
                raise ValueError(f"Value {self.value} is not in possible values {field_spec.possible_values}")

        def as_block_field(self):
            return BlockField(self.name, self.value)

    return FnField


class FnBase:
    @abstractmethod
    def get_blocks(self, next_block: Block, parent: Block) -> list:
        ...


class RawFnBase(FnBase, ABC):
    opcode: str
    inputs: list[FnInput]
    block: Block


def get_raw_fn(fn_spec: FnSpec):
    fields_spec = {name: get_field(field_spec) for name, field_spec in fn_spec.fields.items()}

    class RawFn(RawFnBase):
        def __init__(self, inputs: dict[str, Any], fields: dict[str, Any]):
            self.opcode = fn_spec.opcode
            self.inputs = [FnInput(name, value) for name, value in inputs.items()]
            self.fields: list[FnFieldBase] = []
            for name, field in fields:
                if name not in fields_spec:
                    raise ValueError(f"Unknown field {name}")
                self.fields.append(fields_spec[name](name, field))

        def get_blocks(self, next_block, parent):
            return [Block(
                opcode=self.opcode,
                inputs=[inp.as_block_input() for inp in self.inputs],
                fields=[field.as_block_field() for field in self.fields],
                shadow=False,
                next_block=next_block,
                parent=parent,
            )]

    return RawFn


def get_function(namespace, fn: list[str]) -> FnBase:
    if isinstance(namespace, FnBase):
        if fn is not []:
            raise TypeError("function does not have attributes")
        return namespace
    if fn[0] in namespace:
        return get_function(namespace[fn[0]], fn[1:])