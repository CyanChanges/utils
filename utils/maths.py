from math import gcd
from typing import Protocol

from .decos import except_range

INF = float('INF')


class Fraction(Protocol):
    numerator: int
    denominator: int


@except_range(INF)
def simplify(*nums: int):
    g = gcd(*nums)
    return tuple(int(num / g) for num in nums)


@except_range(2, 1)
def to_float(numerator: int, denominator: int):
    # Fraction(numerator, denominator)
    return numerator / denominator

