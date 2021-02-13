import struct
from shared.lmdb_support import serialize_tuple_of_integers


def test_able_to_serialize():
    data = (2506, 723526)
    expected_output = b'\xca\t\x00\x00\x00\x00\x00\x00F\n\x0b\x00\x00\x00\x00\x00'

    assert serialize_tuple_of_integers(data) == expected_output


def test_serialization_is_correct():
    original_data = (2506, 723526)
    expected_output = b'\xca\t\x00\x00\x00\x00\x00\x00F\n\x0b\x00\x00\x00\x00\x00'
    output = serialize_tuple_of_integers(original_data)
    assert output == expected_output
    assert struct.unpack("<2Q", output) == original_data
