from typing import Optional

from PyScratch.block import Block
from ..lang_types import State
from ..lang_function import FnBase
from ...lang_parser.lang_types import FnCallArgs


class whenflagclicked(FnBase):
    def __init__(self, args: FnCallArgs, state: Optional[State] = None):
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
