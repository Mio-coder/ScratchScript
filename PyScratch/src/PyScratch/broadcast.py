from dataclasses import dataclass

from .primitives import PrimitiveBlock
from .utils import AutoId


@dataclass
class Broadcast(AutoId, PrimitiveBlock):
    name: str

    def as_tuple(self) -> tuple[str, str]:
        return self.item_id, self.name

    def as_list(self):
        return [11, self.name, self.item_id]
