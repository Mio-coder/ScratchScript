from pathlib import Path
from zipfile import ZipFile

from msgspec import DecodeError
from msgspec.json import encode, decode

from block_sb3.load import load


def write_if_changed(file: Path, data):
    try:
        with file.open() as f:
            orig_data = decode(f.read())
    except (DecodeError, FileNotFoundError, OSError):
        changed = True
    else:
        changed = orig_data == data

    if changed:
        with file.open(mode='rw') as f:
            f.write(data)


def run(file: Path, extract: bool = False):
    extract_file = file.with_suffix(".raw.json")
    output = file.with_suffix(".fnspec.json")
    if file.suffix == ".json":
        with file.open() as f:
            data = f.read()
    elif file.suffix in [".zip", ".sb3"]:
        with ZipFile(file) as zipf:
            with zipf.open("project.json", mode="r") as f:
                data = f.read().decode("UTF-8")
    else:
        raise ValueError(f"suffix of {file} must be '.json', '.zip' or '.sb3', not {file.suffix}")

    if extract:
        write_if_changed(extract_file, data)

    functions = load(data)

    write_if_changed(output, encode(functions))
