from typing import Protocol, TypeVar, ParamSpecArgs

T = TypeVar("T", bound=tuple[int, ...])


class Fraction(Protocol):
    numerator: int
    denominator: int


def simplify(*nums: T) -> T:
    pass

def gcd(*nums) -> int:
    pass

