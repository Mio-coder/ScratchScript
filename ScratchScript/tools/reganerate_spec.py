from pathlib import Path
from textwrap import dedent

from msgspec import DecodeError
from msgspec.json import decode, encode

try:
    from block_sb3 import run
except ImportError:
    print("Install block_sb3 to regenerate function specs")
    exit(1)

# optional feature
from hashlib import file_digest


def main(verbose=False):
    dir_path = Path("./src/ScratchScript/function_specs")
    files = [
        "Looks",
        "Motion",
        "Variables"
    ]
    hashes_path = dir_path / "hashes.json"
    if hashes_path.exists():
        try:
            with hashes_path.open() as f:
                hashes = decode(f.read())
        except (DecodeError, OSError):
            hashes = {}
    else:
        hashes = {}
    if verbose:
        print("Hashes:" + "".join([f"\n    {name}: {file_hash}" for name, file_hash in hashes.items()]))
    hash_changed = False
    for file in files:
        path = dir_path / (file + "Blocks.sb3")
        with path.open(mode="rb") as f:
            file_hash = file_digest(f, "sha256").hexdigest()
        if verbose:
            print(dedent(f"""
                Processing file:
                    Name: {file}
                    Path: {path}
                    File hash: {file_hash}
                    Previous file hash: {hashes.get(file, "")} 
            """).strip())
        if file not in hashes or hashes.get(file, "") != file_hash:
            run(path, True)
            hashes[file] = file_hash
            hash_changed = True
            if verbose:
                print("Spec regenerated")
    if hash_changed:
        with hashes_path.open(mode="wb") as f:
            f.write(encode(hashes))
        if verbose:
            print("Hashes updated")


if __name__ == '__main__':
    main()
