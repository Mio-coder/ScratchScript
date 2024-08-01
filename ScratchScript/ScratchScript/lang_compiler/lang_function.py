from abc import abstractmethod
from typing import Type

from PyScratch.PyScratch import Block
from ScratchScript.ScratchScript.lang_compiler.lang_code import State
from ScratchScript.ScratchScript.lang_parser.lang_types import FnCallArgs


class FnBase:
    @abstractmethod
    def __init__(self, raw_fn: FnCallArgs, state: State):
        ...

    @abstractmethod
    def get_blocks(self, next_block: Block, parent: Block) -> list[Block]:
        ...


base_namespace = {}


def get_function(fn: list[str], namespace=None) -> Type[FnBase]:
    namespace = namespace or base_namespace
    while len(fn) > 0:
        if isinstance(namespace, FnBase):
            raise TypeError("function does not have attributes")
        if fn[0] not in namespace:
            raise TypeError(f"namespace {namespace} does not contain an attribute {fn}")
        namespace = get_function(fn[1:], namespace[fn[0]])
    return namespace
