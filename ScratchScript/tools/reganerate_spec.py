from pathlib import Path

try:
    from block_sb3 import run
except ImportError:
    print("Install block_sb3 to regenerate function specs")
    exit(1)


def main():
    dir_path = Path("./src/ScratchScript/function_specs")
    run(dir_path / "LooksBlocks.sb3", True)
    run(dir_path / "MotionBlocks.sb3", True)


if __name__ == '__main__':
    main()
