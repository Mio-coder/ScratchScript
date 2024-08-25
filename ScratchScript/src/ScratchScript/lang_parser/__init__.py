from .lang_lexer import lexer
from .lang_parser import parser
from .lang_types import Code


def parse(source) -> list[Code]:
    token_stream = lexer.lex(source)
    return parser.parse(token_stream)


def main(file):
    with open(file) as f:
        source = f.read() + "\n"
    return parse(source)


if __name__ == '__main__':
    main("../../../example.txt")
