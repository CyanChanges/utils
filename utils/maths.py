from functools import wraps
from typing import Protocol, Never, Callable, Any, TYPE_CHECKING, Type
from math import gcd
import decimal

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
    Fraction()

