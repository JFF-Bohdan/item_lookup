import argparse


def parse_command_line():
    parser = argparse.ArgumentParser(description="Linear search in file")
    parser.add_argument("--input-file", type=str, action="store", required=True)
    return parser.parse_args()
