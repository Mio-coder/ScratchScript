from dataclasses import dataclass

from PyScratch.src.PyScratch.utils import AutoId


@dataclass
class Broadcast(AutoId, short_name="Broadcast"):
    name: str

    def as_tuple(self) -> tuple[str, str]:
        return (self.item_id, self.name)

    def as_list(self):
        return [11, self.name, self.item_id]
