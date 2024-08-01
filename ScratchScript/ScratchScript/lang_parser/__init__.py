from ScratchScript.ScratchScript.lang_parser import lexer
from ScratchScript.ScratchScript.lang_parser.lang_parser import parser


def main(file):
    with open(file) as f:
        source = f.read() + "\n"
    token_stream = lexer.lex(source)
    tokens = list(token_stream)
    result = parser.parse(iter(tokens))
    return result


if __name__ == '__main__':
    main("../../example.txt")
