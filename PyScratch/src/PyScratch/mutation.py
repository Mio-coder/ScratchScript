from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .block import Block


@dataclass
class Mutation:
    block: Optional["Block"] = field(default=None, init=False)  # set by block

    def as_dict(self):
        assert self.block is not None
        result = {
            "tagName": "mutation",
            "chidren": [],
        }
        return result


@dataclass
class Procedure(Mutation):
    name: str
    "%s for string/number input, %b for boolean input"

    def as_dict(self):
        assert self.block is not None
        result = super().as_dict()
        inputs = [inp.name for inp in self.block.inputs]
        result["proccode"] = self.name
        result["argumentids"] = inputs
        return result


@dataclass
class ProcedurePrototypeMutation(Procedure):
    argument_names: list[str]
    argument_deafults: list[str | bool]

    def as_dict(self):
        result = super().as_dict()
        result["argumentnames"] = self.argument_names
        result["argumentdeafults"] = self.argument_deafults
        return result


class ControlStopMutaion(Mutation):
    has_next: bool

    def as_dict(self):
        result = super().as_dict()
        result["has_next"] = self.has_next
        return result
