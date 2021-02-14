import sys
import time
from collections import defaultdict

import humanize

from loguru import logger

from pyroaring import BitMap

from shared.command_line_args_support import base_arg_parser
from shared.memory_usage import get_current_memory_usage
from shared.valid_records_generator import get_all_valid_records

DATA_LIMIT = None

expired_passports = defaultdict(BitMap)


def load_expired_passports_into_roaring_bitmap(input_file: str) -> None:
    records_added = 0

    timestamp_begin = time.monotonic()
    for index, record in enumerate(get_all_valid_records(input_file, logger)):
        if DATA_LIMIT and (index >= DATA_LIMIT):
            break

        expired_passports[record[0]].add(record[1])

        records_added += 1
        if records_added and (not (records_added % 1_000_000)):
            time_elapsed = time.monotonic() - timestamp_begin
            logger.info(
                f"Added records count: {records_added} (time spent: {humanize.precisedelta(time_elapsed)})"
            )

    logger.info(f"Records added: {records_added}")


def is_passport_blocked(series: int, number: int) -> bool:
    if series not in expired_passports:
        return False

    if number not in expired_passports[series]:
        return False

    return True


def main():
    logger.info("Application started")

    parser = base_arg_parser()

    args = parser.parse_args()
    logger.debug(f"args: {args}")

    logger.info("Uploading records into database")
    timestamp_begin = time.monotonic()
    load_expired_passports_into_roaring_bitmap(args.input_file)
    timestamp_end = time.monotonic()

    time_elapsed = timestamp_end - timestamp_begin
    logger.info(f"Time elapsed for data uploading: {humanize.precisedelta(time_elapsed)}")

    while True:
        passport_series = input("Passport series: ")
        passport_number = input("Passport series: ")

        passport_series = passport_series.strip()
        passport_number = passport_number.strip()

        if (not passport_series) and (not passport_number):
            logger.info("Empty request, going exit...")
            break

        passport_series = int(passport_series)
        passport_number = int(passport_number)

        timestamp_begin = time.perf_counter_ns()
        passport_expired = is_passport_blocked(passport_series, passport_number)
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
