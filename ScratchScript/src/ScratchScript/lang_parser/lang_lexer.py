from rply import LexerGenerator
from rply.token import Token, SourcePosition

lg = LexerGenerator()

# Define tokens
keywords = [
    'NEW',
    'VAR',
    'ON',
]
for keyword in keywords:
    lg.add(keyword, keyword)
lg.add('EQ', r'=')
lg.add('DOT', r'\.')
lg.add('COMMA', r',')
lg.add('ADD', r'\+')
lg.add('SUB', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('MOD', r'%')
lg.add('POW', r'\*\*')
lg.add('IN', r'in')
lg.add('L_CURL', r'\{')
lg.add('R_CURL', r'\}')
lg.add('L_PAREN', r'\(')
lg.add('R_PAREN', r'\)')
lg.add('INTEGER', r'\d+')
lg.add('NUMBER', r'\d+(\.\d+)?')
lg.add('STRING', r'"([^"\\]|(\\[\\"nt]))*"')
lg.add('COLOR', r'#[0-9a-zA-Z]{6}')
lg.add('ID', r'[\w_][\w\d_]*')
lg.add('EOL', r'(\n\r|\n|\r)')  # https://stackoverflow.com/a/20056634

# Ignore spaces and newlines
lg.ignore(r'[\t\f\v ]+')
lg.ignore(r'#[^\n\r]*')  # Ignore comments

lexer = lg.build()

lang_tokens = [rule.name for rule in lexer.rules]


def format_tokens(tokens: list[Token]):
    prev_token = Token("", "", SourcePosition(0, 0, 0))
    result = ""
    for token in tokens:
        pos: SourcePosition = token.source_pos
        if prev_token.source_pos.lineno < pos.lineno:
            result += "\n"
            result += " " * pos.colno
        else:
            result += " " * (pos.colno - len(prev_token.value) - prev_token.source_pos.colno + 1)
        result += f"{token.name}:{repr(token.value)[1:-1]}"
        prev_token = token
    return result
