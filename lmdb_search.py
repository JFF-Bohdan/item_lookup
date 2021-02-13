import sys
import time

import humanize

import lmdb

from loguru import logger

from shared.consts import LMDB_DATABASE_FILE
from shared.lmdb_support import serialize_tuple_of_integers
from shared.memory_usage import get_current_memory_usage


def is_passport_expired_lmdb(
        env,
        passport_series: int,
        passport_number: int
) -> bool:
    with env.begin(write=False, buffers=True) as txn:
        query_record = serialize_tuple_of_integers(
            (passport_series, passport_number,)
        )
        result = txn.get(query_record, default=None)

    return result is not None


def main():
    logger.info("Application started")

    logger.info(f"Connecting to the database in file '{LMDB_DATABASE_FILE}'")
    env = lmdb.open(
        LMDB_DATABASE_FILE,
        subdir=False,
        readonly=True,
        lock=False,
        readahead=False,
        meminit=False
    )

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
        passport_expired = is_passport_expired_lmdb(env, passport_series, passport_number)
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
