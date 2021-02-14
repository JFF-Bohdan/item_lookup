import sys
import time
from typing import Dict, Iterator, Tuple

import humanize

from loguru import logger

from shared.command_line_args_support import base_arg_parser
from shared.memory_usage import get_current_memory_usage

from terminaltables import AsciiTable

from tqdm import tqdm

DATA_LIMIT = None


class DataProcessingPipeline(object):
    def __init__(self, file_name: str, data_limit=None):
        self._file_name = file_name
        self._valid_entries_count = 0
        self._invalid_entries_count = 0
        self._data_limit = data_limit

    def run(self):
        for _ in tqdm(self._convert_numbers_to_integers()):
            self._valid_entries_count += 1

    def _convert_numbers_to_integers(self) -> Iterator[Tuple[int, int]]:
        for row in self._filter_for_lines_with_two_columns():
            try:
                result = tuple(int(column) for column in row)
                if (
                        (result[0] > 9999) or
                        (result[1] > 999999) or
                        (str(result[0]).rjust(4, "0") != row[0]) or
                        (str(result[1]).rjust(6, "0") != row[1])
                ):
                    self._invalid_entries_count += 1
                    continue

                yield result
            except ValueError:
                self._invalid_entries_count += 1

    def _filter_for_lines_with_two_columns(self) -> Iterator[Tuple[str, str]]:
        for line in self._yield_strings_from_file():
            line = str(line).strip() if line else line
            if not line:
                self._invalid_entries_count += 1
                continue

            split_data = line.split(",")
            if len(split_data) != 2:
                self._invalid_entries_count += 1
                continue

            yield tuple(split_data)

    def _yield_strings_from_file(self) -> Iterator[str]:
        logger.debug(f"Loading data from file '{self._file_name}'")
        with open(self._file_name, "r", encoding="utf-8") as input_file:
            for index, line in enumerate(input_file):
                # skip header
                if not index:
                    continue

                if self._data_limit and (index >= self._data_limit):
                    break

                yield line

    @property
    def valid_entries_count(self):
        return self._valid_entries_count

    @property
    def invalid_entries_count(self):
        return self._invalid_entries_count


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

    pipeline = DataProcessingPipeline(args.input_file, DATA_LIMIT)

    timestamp_begin = time.perf_counter_ns()
    pipeline.run()
    timestamp_end = time.perf_counter_ns()

    execution_time_ns = (timestamp_end - timestamp_begin)
    execution_time_ms = execution_time_ns / 1_000_000
    execution_time_secs = execution_time_ms / 1_000
    human_readable_memory_usage = humanize.naturalsize(get_current_memory_usage())
    human_readable_execution_time = humanize.naturaldelta(execution_time_secs)

    stat_data = {
        "Valid entries count": pipeline.valid_entries_count,
        "Invalid entries count": pipeline.invalid_entries_count,
        "Execution time (ms)": round(execution_time_ms, 3),
        "Execution time (ns)": execution_time_ns,
        "Execution time (human readable)": human_readable_execution_time,
        "Current memory usage": human_readable_memory_usage
    }

    stat_output = render_stat(stat_data)
    logger.info(f"Execution stat:\n{stat_output}")

    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
