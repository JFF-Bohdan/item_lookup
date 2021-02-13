from typing import Iterator, Tuple

from .file_reader import yield_strings_from_file
from .filtering_and_transformation import convert_to_two_columns_line, convert_tuple_of_strings_to_tuple_of_integers, \
    is_valid_format


def get_all_valid_records(
        input_file: str,
        logger
) -> Iterator[Tuple[int, int]]:
    file_content = yield_strings_from_file(
        file_name=input_file,
        logger=logger,
        records_to_skip=1
    )

    wrong_lines_count = 0
    for line in file_content:
        line = line.strip()
        two_columns_tuple = convert_to_two_columns_line(line)
        if not two_columns_tuple:
            logger.debug(f"Wrong line '{line}': non two columns line")
            wrong_lines_count += 1
            continue

        if not is_valid_format(two_columns_tuple):
            logger.debug(f"Wrong line '{line}': invalid format")
            wrong_lines_count += 1
            continue

        two_columns_tuple = convert_tuple_of_strings_to_tuple_of_integers(two_columns_tuple)

        yield two_columns_tuple

    logger.info(f"Wrong lines count: {wrong_lines_count}")
