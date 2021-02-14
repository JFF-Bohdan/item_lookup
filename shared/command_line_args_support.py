import argparse


def base_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str, action="store", required=True)
    return parser


def add_redis_related_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:

    parser.add_argument(
        "--redis-host",
        type=str,
        action="store",
        required=False,
        default="localhost"
    )

    parser.add_argument(
        "--redis-port",
        type=int,
        action="store",
        required=False,
        default=6379
    )

    parser.add_argument(
        "--redis-database",
        type=int,
        action="store",
        required=False,
        default=1
    )

    return parser


def redis_arg_parser_for_search() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    return add_redis_related_arguments(parser)


def redis_arg_parser_for_creation() -> argparse.ArgumentParser:
    parser = base_arg_parser()
    return add_redis_related_arguments(parser)
