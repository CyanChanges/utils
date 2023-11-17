import importlib
import sys
from typing import Any
from math import ceil


def reload(module_or_name: str | Any):
    if isinstance(module_or_name, str):
        module_or_name = sys.modules.get(module_or_name)

    return importlib.reload(module_or_name)


def self_reload():
    return reload(__name__)


def gen_satisfy_semver(data: bytes) -> tuple[int, int, int]:
    bdata = bin(int(data.hex(), 16))[2:]
    len_bdata = len(bdata)
    block_len = ceil(len_bdata / 3)
    parts = [0, 0, 0]

    parts[0] = bdata[block_len * 2:]
    parts[1] = bdata[block_len * 1:block_len * 2]
    parts[2] = bdata[:block_len * 1]

    ver: tuple = tuple(map(lambda p: int(bin(int(p, 2))[2:], 2), parts))
    return ver


def get_data_from_satisfy_semver(semver: tuple[int, int, int]) -> bytes:
    parts = [0, 0, 0]
    parts[0] = bin(semver[2])[2:]
    parts[1] = bin(semver[1])[2:]
    parts[2] = bin(semver[0])[2:]

    hdata = hex(int(''.join(parts), 2))[2:]
    return bytes.fromhex(hdata)
