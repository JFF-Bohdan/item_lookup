import argparse


def base_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Linear search in file")
    parser.add_argument("--input-file", type=str, action="store", required=True)
    return parser


def sqlite_fs_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Linear search in file")
    parser.add_argument("--input-file", type=str, action="store", required=True)
    return parser
