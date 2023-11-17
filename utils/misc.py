import importlib
import sys
from binascii import crc32
from typing import Any, Self, Optional
from math import ceil
from itertools import chain
from functools import cache


def reload(module_or_name: str | Any):
    if isinstance(module_or_name, str):
        module_or_name = sys.modules.get(module_or_name)

    return importlib.reload(module_or_name)


def self_reload():
    return reload(__name__)


def bin2int(b: str, base=2):
    if b.startswith("0b"):
        return bin2int(b[2:])
    return int(b, base)


def int2bin(n: int):
    return bin(n)[2:]


class SatisfySemVer:
    MASK = (255, 0, 0)

    SUFFIXES = '0123456789abcdefghijklmnopqrstuvwxyz-'

    def __init__(self, data: bytes, t: str = None):
        self.data = data
        self.t = self.SUFFIXES.index(t) if t and t != '-' else self.semver()[3]

    def __repr__(self):
        return f"({self.semver()})<{self.data}>"

    @classmethod
    def _get_mask(cls) -> tuple[int, int, int]:
        return cls.MASK

    @cache
    def semver(self) -> tuple[int, int, int, str]:
        self.t = crc32(self.data).bit_count()
        # binary_data = bin(int(self.data.hex(), 16) << 6 | t)[2:]
        binary_data = int2bin(int(self.data.hex(), 16))
        len_binary = len(binary_data)
        block_len = ceil(len_binary / 3)
        parts = list(self._get_mask())

        parts[0] ^= bin2int(binary_data[:block_len * 1])
        parts[1] ^= bin2int(binary_data[block_len * 1:block_len * 2])
        parts[2] ^= bin2int(binary_data[block_len * 2:])

        ver: tuple = tuple(
            chain(
                parts,
                (self.SUFFIXES[self.t],)
            )
        )
        return ver

    @classmethod
    def from_semver(cls, semver: tuple[int, int, int, Optional[str]] | tuple[int, int, int]) -> Self:
        parts = list(cls._get_mask())
        t = -1
        if len(semver) == 4 and isinstance(semver, str):
            t = cls.SUFFIXES.index(semver[3])

        parts[0] ^= semver[0]
        parts[1] ^= semver[1]
        parts[2] ^= semver[2]

        hex_data = hex(bin2int(''.join(map(int2bin, parts))))[2:]
        data = bytes.fromhex(hex_data)
        if t != -1 and t != crc32(data).bit_count():
            raise ValueError(f"Verify failed {t} != {crc32(data).bit_count()}")
        return cls(data, cls.SUFFIXES[t])


def semver_stringify(semver: tuple[int, int, int, Optional[str]] | tuple[int, int, int]) -> str:
    return '-'.join(('.'.join(map(str, semver[:3])), *semver[3:]))


def to_semver(semver: str):
    ver, *suffix = semver.split('-')
    return tuple(chain(map(int, ver.split('.')), suffix))
