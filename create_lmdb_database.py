import os
import sys
import time

import humanize

import lmdb

from loguru import logger

from shared.command_line_args_support import base_arg_parser
from shared.consts import LMDB_DATABASE_FILE
from shared.lmdb_support import serialize_tuple_of_integers
from shared.valid_records_generator import get_all_valid_records

DATA_LIMIT = None


def load_records_into_lmdb_database(database_path: str, input_file: str) -> None:
    records_added = 0
    env = lmdb.open(
        database_path,
        subdir=False,
        readonly=False,
        lock=True,
        readahead=False,
        meminit=False,
        map_size=int(6e9)
    )

    timestamp_begin = time.monotonic()
    with env.begin(write=True, buffers=True) as txn:
        for index, record in enumerate(get_all_valid_records(input_file, logger)):
            if DATA_LIMIT and (index >= DATA_LIMIT):
                break

            record = serialize_tuple_of_integers(record)
            txn.put(record, bytes([0x01]))

            records_added += 1
            if records_added and (not (records_added % 1_000_000)):
                time_elapsed = time.monotonic() - timestamp_begin
                logger.info(
                    f"Added records count: {records_added} (time spent: {humanize.precisedelta(time_elapsed)})"
                )

    logger.info(f"Records added: {records_added}")


def main():
    logger.info("Application started")

    parser = base_arg_parser()

    args = parser.parse_args()
    logger.debug(f"args: {args}")

    if os.path.exists(LMDB_DATABASE_FILE):
        logger.warning(f"Removing file {LMDB_DATABASE_FILE}")
        os.remove(LMDB_DATABASE_FILE)

    database_file_name_without_extension, _ = os.path.splitext(LMDB_DATABASE_FILE)
    lock_file = database_file_name_without_extension + ".lmdb-lock"
    if os.path.exists(lock_file):
        logger.warning(f"Removing file {lock_file}")
        os.remove(lock_file)

    logger.debug(f"lock_file: {lock_file}")

    db_dir = os.path.dirname(LMDB_DATABASE_FILE)
    logger.debug(f"Database directory: {db_dir}")

    if not os.path.exists(db_dir):
        logger.info(f"Making directory '{db_dir}'")
        os.makedirs(db_dir)

    logger.info("Uploading records into database")
    timestamp_begin = time.monotonic()
    load_records_into_lmdb_database(LMDB_DATABASE_FILE, args.input_file)
    timestamp_end = time.monotonic()

    time_elapsed = timestamp_end - timestamp_begin
    logger.info(f"Time elapsed: {humanize.precisedelta(time_elapsed)}")

    logger.info("Application finished")


if __name__ == "__main__":
    main()
    sys.exit(0)
