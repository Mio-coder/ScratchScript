from dataclasses import dataclass
from typing import Sequence, TypeVar, Generic


@dataclass
class IDTemplate:
    prefix: str
    count: int = 0

    def get(self):
        self.count += 1
        return self.prefix + str(self.count)


T = TypeVar("T")


class AutoId(Generic[T]):
    id_template = IDTemplate("Id")

    def __post_init__(self):
        self.item_id = self.id_template.get()

    def __init_subclass__(cls) -> None:
        cls.id_template = IDTemplate(cls.__name__)

    def get(self) -> T:
        return None

    def as_tuple(self) -> tuple[str, T]:
        return self.item_id, self.get()


def from_dict(data: Sequence[AutoId[T]]) -> dict[str, T]:
    return dict(map(lambda x: x.as_tuple(), data))
