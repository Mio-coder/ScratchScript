from PyScratch.PyScratch import Block, InputType, BlockInput, BlockField
from ScratchScript.ScratchScript.lang_compiler.lang_function import FnBase
from ScratchScript.ScratchScript.lang_parser.lang_types import FnCallArgs
from ScratchScript.ScratchScript.lang_compiler.lang_code import State


class setvariableto(FnBase):
    def __init__(self, args: FnCallArgs, state: State):
        self.value = args.args[0]
        self.variable = state.get(args.args[1])

    def get_blocks(self, next_block: Block, parent: Block) -> list:
        return [Block(
            opcode="data_setvariableto",
            inputs=[
                BlockInput("VALUE", InputType.no_shadow, self.value)
            ],
            fields=[
                BlockField("VARIABLE")
            ],
            shadow=False,
            next_block=next_block,
            parent=parent,
        )]
