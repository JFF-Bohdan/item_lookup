import sys
import time
from typing import Dict

import humanize

from loguru import logger

from shared.command_line_args_support import base_arg_parser
from shared.filtering_and_transformation import convert_to_two_columns_line, \
    convert_tuple_of_strings_to_tuple_of_integers, is_valid_format
from shared.memory_usage import get_current_memory_usage

from terminaltables import AsciiTable

from tqdm import tqdm


valid_entries_count = 0
invalid_entries_count = 0


def count_records_stat(input_file: str):
    global invalid_entries_count
    global valid_entries_count

    with open(input_file, "r", encoding="utf-8") as input_file:
        for index, line in enumerate(tqdm(input_file)):
            # skipping header
            if not index:
                continue

            two_columns_tuple = convert_to_two_columns_line(line)
            if not two_columns_tuple:
                invalid_entries_count += 1
                continue

            if not is_valid_format(two_columns_tuple):
                invalid_entries_count += 1
                continue

            _ = convert_tuple_of_strings_to_tuple_of_integers(two_columns_tuple)
            valid_entries_count += 1


def render_stat(stat_dict: Dict) -> str:
    data = [["Parameter", "Value"]]
    for k, v in stat_dict.items():
        data.append([k, v])

    table = AsciiTable(data)
    return table.table


def main():
    logger.info("Application started")

    parser = base_arg_parser()

    args = parser.parse_args()
    logger.debug(f"args: {args}")

    timestamp_begin = time.perf_counter_ns()
    count_records_stat(args.input_file)
    timestamp_end = time.perf_counter_ns()

    execution_time_ns = (timestamp_end - timestamp_begin)
    execution_time_ms = execution_time_ns / 1_000_000
    human_readable_memory_usage = humanize.naturalsize(get_current_memory_usage())

    stat_data = {
        "Valid entries count": valid_entries_count,
        "Invalid entries count": invalid_entries_count,
        "Execution time (ms)": round(execution_time_ms, 3),
        "Execution time (ns)": execution_time_ns,
        "Current memory usage": human_readable_memory_usage
    }

    stat_output = render_stat(stat_data)
    logger.info(f"Execution stat:\n{stat_output}")

    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
