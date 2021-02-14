import sys
import time

import humanize

from loguru import logger

import redis

from shared.command_line_args_support import redis_arg_parser_for_creation
from shared.valid_records_generator import get_all_valid_records

DATA_LIMIT = None


def load_records_into_redis_database(redis_connection, input_file: str) -> None:
    records_added = 0
    pipeline_length = 0
    pipeline = redis_connection.pipeline()
    max_pipeline_length = 250_000

    timestamp_begin = time.monotonic()
    for index, record in enumerate(get_all_valid_records(input_file, logger)):
        if DATA_LIMIT and (index >= DATA_LIMIT):
            break

        redis_key = f"IS_{record[0]}"
        pipeline.setbit(redis_key, record[1], 1)
        pipeline_length += 1

        if pipeline_length >= max_pipeline_length:
            pipeline.execute()
            pipeline_length = 0

        records_added += 1
        if records_added and (not (records_added % 1_000_000)):
            time_elapsed = time.monotonic() - timestamp_begin
            logger.info(
                f"Added records count: {records_added} (time spent: {humanize.precisedelta(time_elapsed)})"
            )

    if pipeline_length:
        pipeline.execute()

    logger.info(f"Records added: {records_added}")


def main():
    logger.info("Application started")

    parser = redis_arg_parser_for_creation()

    args = parser.parse_args()
    logger.debug(f"args: {args}")

    logger.info("Connecting to redis ")
    redis_connection = redis.Redis(
        host=args.redis_host,
        port=args.redis_port,
        db=args.redis_database
    )

    logger.info("Uploading records into database")
    timestamp_begin = time.monotonic()
    load_records_into_redis_database(redis_connection, args.input_file)
    timestamp_end = time.monotonic()

    time_elapsed = timestamp_end - timestamp_begin
    logger.info(f"Time elapsed: {humanize.precisedelta(time_elapsed)}")

    redis_connection.close()
    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
