from abc import abstractmethod
from typing import Type, Optional

from PyScratch.block import Block
from .lang_types import State
from ..lang_parser.lang_types import FnCallArgs, FnCall


class FnBase:
    @abstractmethod
    def __init__(self, args: FnCallArgs, state: Optional[State] = None):
        ...

    @abstractmethod
    def get_blocks(self, next_block: Block, parent: Block) -> list[Block]:
        ...


base_namespace: dict[str, dict[str, Type[FnBase] | dict]] = {}


class ModuleNamespace:
    parent_namespace = base_namespace

    def __init__(self, name: str):
        self.namespace = self.parent_namespace[name] = dict()

    def __setitem__(self, key: str, value: Type[FnBase]):
        self.namespace[key] = value

    def register(self, name, value=None):
        def inner(v):
            self.namespace[name] = v

        if value is not None:
            return inner(value)
        return inner


def get_function(fn: list[str], namespace=None) -> Type[FnBase]:
    namespace = namespace or base_namespace
    while len(fn) > 0:
        if isinstance(namespace, FnBase):
            raise TypeError("function does not have attributes")
        if fn[0] not in namespace:
            raise TypeError(f"namespace {namespace} does not contain an attribute {fn}")
        namespace = get_function(fn[1:], namespace[fn[0]])
    return namespace


def parse_fn(fn: FnCall, state: Optional[State] = None) -> FnBase:
    return get_function(fn.name)(fn.args, state)
