from typing import Optional, Set, Tuple


def convert_to_two_columns_line(line: str) -> Optional[Tuple[str, str]]:
    line = str(line).strip() if line else line
    if not line:
        return None

    split_data = tuple(item.strip() for item in line.split(",") if item.strip())
    if len(split_data) != 2:
        return None

    return split_data


def is_valid_number_item(value: str, required_length: int, valid_symbols: Set[str]) -> bool:
    if len(value) != required_length:
        return False

    return all(char in valid_symbols for char in value)


def is_valid_format(row: Tuple[str, str]) -> bool:
    valid_symbols = {str(index) for index in range(10)}

    required_lengths = [4, 6]
    for column_index, column in enumerate(row):
        if not is_valid_number_item(column, required_lengths[column_index], valid_symbols):
            return False

    return True


def convert_tuple_of_strings_to_tuple_of_integers(row: Tuple[str, str]) -> Tuple[int, int]:
    return tuple(int(column) for column in row)
