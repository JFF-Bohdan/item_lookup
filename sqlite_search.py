import sqlite3
import sys
import time

import humanize

from loguru import logger

from shared.consts import DATABASE_FILE
from shared.memory_usage import get_current_memory_usage

SQL_CHECK_IF_EXISTS = """
select * from expired_passports
where
    (passport_series=?)
    and (passport_number=?)
"""


def is_passport_expired_sqlite(
        connection,
        passport_series: int,
        passport_number: int
) -> bool:
    data = connection.execute(SQL_CHECK_IF_EXISTS, [passport_series, passport_number])
    logger.debug(f"data: {data}")
    return False


def main():
    logger.info("Application started")

    logger.info(f"Connecting to the database in file '{DATABASE_FILE}'")
    connection = sqlite3.connect(DATABASE_FILE)

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
        passport_expired = is_passport_expired_sqlite(connection, passport_series, passport_number)
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
