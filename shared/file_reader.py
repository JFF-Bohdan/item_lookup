from typing import Iterator


def yield_strings_from_file(
        file_name: str,
        logger,
        records_to_skip: int = 1
) -> Iterator[str]:
    logger.info(f"Loading data from file '{file_name}'")
    loaded_lines_count = 0
    with open(file_name, "r", encoding="utf-8") as input_file:
        for index, line in enumerate(input_file, start=1):
            if index <= records_to_skip:
                continue

            loaded_lines_count += 1
            yield line

    logger.info(f"Loaded lines count: {loaded_lines_count}")
