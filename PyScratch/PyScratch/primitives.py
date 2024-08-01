from abc import abstractmethod
from dataclasses import dataclass


class PrimitiveBlock:

    @abstractmethod
    def as_list(self) -> list:
        ...


@dataclass
class Number(PrimitiveBlock):
    value: float

    def as_list(self):
        return [4, self.value]


@dataclass
class Positive(PrimitiveBlock):
    value: int

    def as_list(self):
        return [5, self.value]


@dataclass
class Negative(PrimitiveBlock):
    value: int

    def as_list(self):
        return [6, self.value]


@dataclass
class Integer(PrimitiveBlock):
    value: int

    def as_list(self):
        return [7, self.value]


@dataclass
class Angle(PrimitiveBlock):
    value: int

    def as_list(self):
        return [8, self.value]


@dataclass
class Color(PrimitiveBlock):
    value: str
    "in #hex"

    def as_list(self):
        return [9, self.value]


@dataclass
class String(PrimitiveBlock):
    value: str

    def as_list(self):
        return [10, self.value]
