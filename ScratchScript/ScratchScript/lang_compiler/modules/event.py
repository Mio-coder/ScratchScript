from PyScratch.PyScratch import Block
from ScratchScript.ScratchScript.lang_compiler.lang_code import State
from ScratchScript.ScratchScript.lang_compiler.lang_function import FnBase
from ScratchScript.ScratchScript.lang_parser.lang_types import FnCallArgs


class whenflagclicked(FnBase):
    def __init__(self, args: FnCallArgs, state: State):
        pass

    def get_blocks(self, next_block: Block, parent: Block) -> list:
        return [Block(
            opcode="event_whenflagclicked",
            inputs=[],
            fields=[],
            shadow=False,
            next_block=next_block,
            parent=parent,
        )]


MAIN_CODE_EVENT = whenflagclicked(FnCallArgs(), State())


class whenthisspriteclicked(FnBase):
    def __init__(self, args: FnCallArgs, state: State):
        pass

    def get_blocks(self, next_block: Block, parent: Block) -> list:
        return [Block(
            opcode="event_whenthisspriteclicked",
            inputs=[],
            fields=[],
            shadow=False,
            next_block=next_block,
            parent=parent,
        )]
