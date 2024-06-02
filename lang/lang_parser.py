from functools import wraps

from rply import ParserGenerator

from lang.lang_lexer import lang_tokens, lexer

pg = ParserGenerator(lang_tokens)


def log_call(fn):
    @wraps(fn)
    def wrapper(p):
        print(f"function {fn.__name__} got called with {' '.join(map(str, p))}")
        return fn(p)

    return wrapper


class Node:
    def __init__(self, type_, **kwargs):
        self.type = type_
        self.values = kwargs

    def __setitem__(self, key, value):
        self.values[key] = value

    def __getitem__(self, item):
        return self.values[item]

    def __repr__(self):
        return f"Node(type={self.type}, value={self.values})"


@pg.production('program : statements')
@log_call
def program(p):
    return Node('program', code=p[0])


@pg.production('statements : statements statement')
@log_call
def statements(p):
    return p[0] + [p[1]]


@pg.production('statements : statement')
@log_call
def statements(p):
    return [p[0]]


@pg.production('statement : broadcast_stmt')
@pg.production('statement : var_stmt')
@pg.production('statement : sprite_stmt')
@log_call
def statement(p):
    return p[0]


@pg.production('statement : EOL')
@log_call
def statement(p):
    return []


@pg.production('broadcast_stmt : BROADCAST ID EOL')
@log_call
def broadcast(p):
    return Node('broadcast_stmt', name=p[1].getstr())


@pg.production('var_stmt : VAR ID EQ value EOL')
@pg.production('var_stmt : VAR ID EOL')
@log_call
def var(p):
    node = Node('var_stmt', name=p[1].getstr())
    if len(p) == 5:
        node["init_value"] = p[3]
    return node


@pg.production('sprite_stmt : SPRITE ID L_CURL sprite_content R_CURL EOL')
@log_call
def sprite(p):
    return Node('sprite_stmt', name=p[1].getstr(), body=p[3])


@pg.production('sprite_content : sprite_content sprite_content_stmt')
@log_call
def sprite_content(p):
    return p[0] + [p[1]]


@pg.production('sprite_content : sprite_content_stmt')
@log_call
def sprite_content(p):
    if p[0] is not None:
        return [p[0]]
    else:
        return []


@pg.production('sprite_content_stmt : costume_stmt')
@pg.production('sprite_content_stmt : sound_stmt')
@pg.production('sprite_content_stmt : event_stmt')
@pg.production('sprite_content_stmt : code')
@log_call
def sprite_content(p):
    return p[0]


@pg.production('sprite_content_stmt : EOL')
@log_call
def sprite_content(p):
    return None


@pg.production('event_stmt : ON fn_call L_CURL code R_CURL EOL')
@log_call
def event(p):
    return Node('event', name=p[1], code=p[3])


@pg.production('code : code code_stmt')
@log_call
def code(p):
    return p[0] + [p[1]]


@pg.production('code : code_stmt')
@log_call
def code(p):
    if p[0] is not None:
        return [p[0]]
    return []


@pg.production('code_stmt : var_stmt')
@pg.production('code_stmt : fn_call EOL')
@pg.production('code_stmt : assign')
@pg.production('code_stmt : event_stmt')
@log_call
def code(p):
    return p[0]


@pg.production("assign : attr EQ expr EOL")
@log_call
def assign(p):
    return Node('assignment', name=p[0], value=p[2])


@pg.production('code_stmt : EOL')
@log_call
def code(p):
    return None


@pg.production('fn_call : attr L_PAREN fn_call_args R_PAREN')
@log_call
def fn_call(p):
    return Node('fn_call', name=p[0], args=p[2])


@pg.production('fn_call : attr L_PAREN R_PAREN')
@log_call
def fn_call(p):
    return Node('fn_call', name=p[0], args=[])


@pg.production('fn_call_args : expr')
@pg.production('fn_call_args : fn_call_args COMMA expr')
@log_call
def fn_call_args(p):
    if len(p) == 1:
        return [p[0]]
    return p[0] + [p[2]]


@pg.production('attr : ID')
@pg.production('attr : attr DOT ID')
@log_call
def attr(p):
    if len(p) == 1:
        return Node('attr', value=[p[0].getstr()])
    p[0]["value"].append(p[2].getstr())
    return p[0]


@pg.production('expr : attr')
@pg.production('expr : value')
@pg.production('expr : L_PAREN expr biop expr R_PAREN')
@pg.production('expr : L_PAREN unop expr R_PAREN')
@log_call
def expr(p):
    if len(p) == 1:
        return p[0]
    if len(p) == 3:
        return Node('expr', left=None, op=p[1].getstr(), right=p[2])
    return Node('expr', left=p[1], op=p[2].getstr(), right=p[3])


@pg.production('biop : ADD')
@pg.production('biop : SUB')
@pg.production('biop : MUL')
@pg.production('biop : DIV')
@pg.production('biop : MOD')
@pg.production('biop : POW')
@pg.production('biop : IN')
@log_call
def biop(p):
    return p[0]


@pg.production('unop : SUB')
@log_call
def unop(p):
    return p[0]


@pg.production('costume_stmt : COSTUME ID L_PAREN fields R_PAREN EOL')
@log_call
def costume(p):
    return Node('costume', name=p[1].getstr(), fields=p[3])


@pg.production('sound_stmt : SOUND ID L_PAREN fields R_PAREN EOL')
@log_call
def sound(p):
    return Node('sound', name=p[1].getstr(), fields=p[3])


@pg.production('fields : fields field_stmt')
@log_call
def fields(p):
    p[0][p[1][0]] = p[1][1]
    return p[0]


@pg.production('fields : field_stmt')
@log_call
def fields(p):
    return {p[0][0]: p[0][1]}


@pg.production('fields : EOL')
@log_call
def fields(p):
    return {}


@pg.production('field_stmt : ID EQ value EOL')
@log_call
def field(p):
    return p[0].getstr(), p[2]


@pg.production('value : NUMBER')
@log_call
def value(p):
    return float(p[0].getstr())


@pg.production('value : STRING')
@log_call
def value(p):
    return p[0].getstr()


@pg.production('value : COLOR')
@log_call
def value(p):
    return p[0].getstr()


@pg.production('value : position')
@log_call
def value(p):
    return p[0]


@pg.production('position : L_PAREN NUMBER COMMA NUMBER R_PAREN')
@log_call
def position(p):
    return float(p[1].getstr()), float(p[3].getstr())


parser = pg.build()


def main():
    with open("example.txt") as f:
        source = f.read() + "\n"
    token_stream = lexer.lex(source)
    tokens = list(token_stream)
    # print(print_tokens(tokens))
    result = parser.parse(iter(tokens))
    print(result)


if __name__ == '__main__':
    main()
