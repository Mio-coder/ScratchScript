from argparse import ArgumentParser
from pathlib import Path

from . import run


def parse_args():
    parser = ArgumentParser("block-sb3")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("-e", "--extract", action="store_true", help="extract raw json")
    return parser.parse_args()


def main():
    args = parse_args()
    run(args.input_file, args.extract)
    return 0
