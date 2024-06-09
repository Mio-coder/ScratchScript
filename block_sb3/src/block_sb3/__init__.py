from zipfile import ZipFile

from msgspec.json import encode

from block_sb3.load import load


def run(file, extract: bool = False):
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
        with extract_file.open(mode='w') as f:
            f.write(data)
    functions = load(data)

    with output.open(mode="wb") as f:
        f.write(encode(functions))
