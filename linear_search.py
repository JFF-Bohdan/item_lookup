import sys
import time

import humanize

from loguru import logger

from shared.command_line_args_support import base_arg_parser
from shared.memory_usage import get_current_memory_usage


def is_passport_expired(
        input_file: str,
        passport_series: str,
        passport_number: str
) -> bool:
    with open(input_file, "r", encoding="utf-8") as input_file:
        for index, line in enumerate(input_file):
            if not index:
                continue

            items = [item.strip() for item in line.split(",")]
            if len(items) != 2:
                continue

            if(
                    (items[0] == passport_series) and
                    (items[1] == passport_number)
            ):
                return True

    return False


def main():
    logger.info("Application started")

    parser = base_arg_parser()

    args = parser.parse_args()
    logger.debug(f"args: {args}")

    while True:
        passport_series = input("Passport series: ")
        passport_number = input("Passport series: ")

        passport_series = passport_series.strip()
        passport_number = passport_number.strip()

        if (not passport_series) and (not passport_number):
            logger.info("Empty request, going exit...")
            break

        timestamp_begin = time.perf_counter_ns()
        passport_expired = is_passport_expired(args.input_file, passport_series, passport_number)
        timestamp_end = time.perf_counter_ns()

        lookup_time_ns = (timestamp_end - timestamp_begin)
        lookup_time_ms = lookup_time_ns / 1_000_000
        logger.info(
            f"Lookup time {round(lookup_time_ms, 3)} ms ({lookup_time_ns} ns). Is passport expired: {passport_expired}"
        )

    human_readable_memory_usage = humanize.naturalsize(get_current_memory_usage())
    logger.info(f"Used memory: {human_readable_memory_usage}")

    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
