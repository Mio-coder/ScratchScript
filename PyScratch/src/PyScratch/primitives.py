from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class Number:
    value: float

    def as_list(self):
        return [4, self.value]


@dataclass
class Positive:
    value: int

    def as_list(self):
        return [5, self.value]


@dataclass
class Negative:
    value: int

    def as_list(self):
        return [6, self.value]


@dataclass
class Integer:
    value: int

    def as_list(self):
        return [7, self.value]


@dataclass
class Angle:
    value: int

    def as_list(self):
        return [8, self.value]


@dataclass
class Color:
    value: str
    "in #hex"

    def as_list(self):
        return [9, self.value]


@dataclass
class String:
    value: str

    def as_list(self):
        return [10, self.value]


@runtime_checkable
class PrimitiveBlock(Protocol):

    def as_list(self) -> list:
        ...
