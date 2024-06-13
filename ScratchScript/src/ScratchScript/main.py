from ScratchScript.lang_compiler.lang_extract import parse_program
from lang_parser import main as parser_main


def main(file):
    parse_program(
        parser_main(file)
    )


if __name__ == '__main__':
    main("example2.txt")