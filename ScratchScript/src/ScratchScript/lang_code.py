from pathlib import Path
from typing import Optional

from msgspec import Struct
from msgspec.json import decode


class FnInput(Struct):
    name: str
    block_opcode: Optional[str] = None


class FnFields(Struct):
    name: str
    possible_values: set
    functions: set["FnSpec"] = set()


class FnSpec(Struct):
    opcode: str
    inputs: dict[str, FnInput]
    fields: dict[str, FnFields]


class ModuleSpec(Struct):
    functions: dict[str, FnSpec]


specs_dir = Path(__file__).parent / "function_specs"


def get_spec(spec_name) -> ModuleSpec:
    file = specs_dir / (spec_name + ".fnspec.json")
    with file.open() as f:
        return decode(f.read(), type=ModuleSpec)

