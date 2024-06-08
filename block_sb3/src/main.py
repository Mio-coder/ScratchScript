from pathlib import Path
from sys import argv
from zipfile import ZipFile

from msgspec.json import encode

from load import load


def main():
    if len(argv) != 3:
        print(f"Usage `block-sb3 [input_file] [output_file]`")
        return 1
    file = Path(argv[1])
    output = Path(argv[2])
    if not file.is_file():
        print(f"{file} is not a valid path")
        return 1
    if not output.is_file():
        print(f"{output} is not a valid path")
        return 1
    if file.suffix == ".json":
        with file.open() as f:
            functions = load(f.read())
    elif file.suffix in [".zip", ".sb3"]:
        with ZipFile(file) as zipf:
            with zipf.open("project.json") as f:
                functions = load(f.read())
    else:
        print(f"suffix of {file} must be '.json', '.zip' or '.sb3', not {file.suffix}")
        return 1

    with output.open(mode="wb") as f:
        f.write(encode(functions))
    return 0
