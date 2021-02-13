import os
import sqlite3
import sys
import time

import humanize

from loguru import logger

from shared.command_line_args_support import base_arg_parser
from shared.consts import DATABASE_FILE
from shared.valid_records_generator import get_all_valid_records

SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS expired_passports
(
    passport_series integer,
    passport_number integer,
    PRIMARY KEY (passport_series, passport_number)
);
"""

SQL_INSERT_ITEM = """
INSERT INTO expired_passports(passport_series, passport_number)
values(?, ?);
"""

DATA_LIMIT = None


def load_records_into_database(connection, input_file: str) -> None:
    chunk_to_add = []
    max_chunk_size = 50_000

    records_added = 0
    for index, record in enumerate(get_all_valid_records(input_file, logger)):
        if DATA_LIMIT and (index >= DATA_LIMIT):
            break

        chunk_to_add.append(record)
        if len(chunk_to_add) >= max_chunk_size:
            connection.executemany(SQL_INSERT_ITEM, chunk_to_add)
            chunk_to_add = []

        records_added += 1
        if records_added and (not (records_added % 1_000_000)):
            logger.info(f"Added records count: {records_added}")

    if chunk_to_add:
        connection.executemany(SQL_INSERT_ITEM, chunk_to_add)

    logger.info(f"Records added: {records_added}")


def main():
    logger.info("Application started")

    parser = base_arg_parser()

    args = parser.parse_args()
    logger.debug(f"args: {args}")

    if os.path.exists(DATABASE_FILE):
        logger.info(f"Removing file {DATABASE_FILE}")
        os.remove(DATABASE_FILE)

    db_dir = os.path.dirname(DATABASE_FILE)
    logger.debug(f"Database directory: {db_dir}")

    if not os.path.exists(db_dir):
        logger.warning(f"Making directory '{db_dir}'")
        os.makedirs(db_dir)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.execute(SQL_CREATE_TABLE)

    logger.info("Uploading records into database")
    timestamp_begin = time.monotonic()
    load_records_into_database(connection, args.input_file)
    timestamp_end = time.monotonic()

    time_elapsed = timestamp_end - timestamp_begin
    logger.info(f"Time elapsed: {humanize.precisedelta(time_elapsed)}")

    connection.commit()
    connection.close()

    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
