import struct
from typing import Tuple


def serialize_tuple_of_integers(value: Tuple[int, int]) -> bytes:
    return struct.pack("<2Q", *value)
