import importlib
import sys
from binascii import crc32
from typing import Any, Self, Optional, TypeGuard
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


class SatisfySemver:
    VERSION = 2

    MASK = (255, 0, 0)

    SUFFIXES = '0123456789abcdefghijklmnopqrstuvwxyz-'

    PART_SZ = 8

    def __init__(self, data: bytes, t: str = None, c=VERSION):
        self.data = data
        self.version = c
        self.t = self.SUFFIXES.index(t) if t and t.startswith('-') else self.semver()[3]

    def __repr__(self):
        return f"({self.semver()})<{self.data}>"

    @classmethod
    def has_t(cls, semver: tuple[int, int, int] | tuple[int, int, int, Optional[str]]) \
            -> TypeGuard[tuple[int, int, int, str]]:
        return len(semver) == 4 and isinstance(semver[3], str)

    @classmethod
    def _get_mask(cls) -> tuple[int, int, int]:
        return cls.MASK

    @cache
    def semver(self) -> tuple[int, int, int, str]:
        self.t = crc32(self.data).bit_count()
        # binary_data = bin(int(self.data.hex(), 16) << 6 | t)[2:]
        binary_data = int2bin(int(self.data.hex(), 16))
        len_binary = len(binary_data)
        block_sz = ceil(len_binary / 3)
        binary_data = binary_data.zfill(ceil(len_binary / 3) * 3)
        sz_block_sz = self.PART_SZ + ceil(block_sz.bit_length() / self.PART_SZ) - 1
        parts = list(self._get_mask())

        parts[0] ^= bin2int(binary_data[:block_sz * 1])
        parts[1] ^= bin2int(binary_data[block_sz * 1:block_sz * 2])
        parts[2] ^= bin2int(binary_data[block_sz * 2:])
        parts[2] <<= sz_block_sz
        parts[2] |= block_sz

        semver: tuple = tuple(
            chain(
                parts,
                (self.SUFFIXES[self.t] + self.SUFFIXES[ceil(sz_block_sz / self.PART_SZ) - 1],)
            )
        )
        return semver

    @classmethod
    def from_semver(cls, semver: tuple[int, int, int, Optional[str]] | tuple[int, int, int]) -> Self:
        parts = list(cls._get_mask())
        t = -1
        sz_block_sz = cls.PART_SZ
        if cls.has_t(semver):
            semver: tuple[int, int, int, str]
            if len(semver[3]) == 0:
                return cls.from_semver_v1(semver)
            t = cls.SUFFIXES.index(semver[3][0])
            sz_block_sz += (cls.SUFFIXES.index(semver[3][1]) * cls.PART_SZ)

        parts[0] ^= semver[0]
        parts[1] ^= semver[1]
        parts[2] ^= semver[2]
        block_sz = parts[2] & bin2int('1' * sz_block_sz)
        parts[2] >>= sz_block_sz

        hex_data = hex(bin2int(''.join(map(lambda x: int2bin(x).zfill(block_sz), parts))))[2:]
        data = bytes.fromhex(hex_data)
        if t != -1 and t != crc32(data).bit_count():
            raise ValueError(f"Verify failed: {t} != {crc32(data).bit_count()}")
        return cls(data, cls.SUFFIXES[t], cls.VERSION)

    @classmethod
    def from_semver_v1(cls, semver: tuple[int, int, int, Optional[str]] | tuple[int, int, int]) -> Self:
        parts = list(cls._get_mask())
        t = -1
        if cls.has_t(semver):
            semver: tuple[int, int, int, str]
            t = cls.SUFFIXES.index(semver[3][0])

        parts[0] ^= semver[0]
        parts[1] ^= semver[1]
        parts[2] ^= semver[2]

        hex_data = hex(bin2int(''.join(map(int2bin, parts))))[2:]
        data = bytes.fromhex(hex_data)
        if t != -1 and t != crc32(data).bit_count():
            raise ValueError(f"Verify failed: {t} != {crc32(data).bit_count()}")
        return cls(data, cls.SUFFIXES[t], 1)


def semver_stringify(semver: tuple[int, int, int, Optional[str]] | tuple[int, int, int]) -> str:
    return '-'.join(('.'.join(map(str, semver[:3])), *semver[3:]))


def to_semver(semver: str):
    ver, *suffix = semver.split('-')
    return tuple(chain(map(int, ver.split('.')), suffix))
