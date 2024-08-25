from typing import Optional

from PyScratch.block import Block, InputType, BlockInput, BlockField
from ..lang_function import FnBase, ModuleNamespace
from ..lang_types import State
from ...lang_parser.lang_types import FnCallArgs

ns = ModuleNamespace("data")


@ns.register("setvariableto")
class setvariableto(FnBase):
    def __init__(self, args: FnCallArgs, state: Optional[State] = None):
        assert state is not None, "This function requires state"
        self.value = args.args[0]
        self.variable = state.get(args.args[1])

    def get_blocks(self, next_block: Block, parent: Block) -> list:
        return [Block(
            opcode="data_setvariableto",
            inputs=[
                BlockInput("VALUE", InputType.no_shadow, self.value)
            ],
            fields=[
                BlockField("VARIABLE", self.variable)
            ],
            shadow=False,
            next_block=next_block,
            parent=parent,
        )]
