import sys
import time

import humanize

from loguru import logger

import redis

from shared.command_line_args_support import redis_arg_parser_for_search
from shared.memory_usage import get_current_memory_usage


def is_passport_expired_redis(
        redis_connection,
        passport_series: int,
        passport_number: int
) -> bool:
    redis_key = f"IS_{passport_series}"
    logger.debug(f"redis_key is '{redis_key}'")
    redis_result = redis_connection.getbit(redis_key, passport_number)
    logger.debug(f"redis_result: {redis_result}")
    return redis_result == 1


def main():
    logger.info("Application started")

    parser = redis_arg_parser_for_search()
    args = parser.parse_args()
    logger.debug(f"args: {args}")

    logger.info("Connecting to redis ")
    redis_connection = redis.Redis(
        host=args.redis_host,
        port=args.redis_port,
        db=args.redis_database
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
        passport_expired = is_passport_expired_redis(redis_connection, passport_series, passport_number)
        timestamp_end = time.perf_counter_ns()

        lookup_time_ns = (timestamp_end - timestamp_begin)
        lookup_time_ms = lookup_time_ns / 1_000_000
        logger.info(
            f"Lookup time {round(lookup_time_ms, 3)} ms ({lookup_time_ns} ns). Is passport expired: {passport_expired}"
        )

    human_readable_memory_usage = humanize.naturalsize(get_current_memory_usage())
    logger.info(f"Used memory: {human_readable_memory_usage}")
    redis_connection.close()

    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
