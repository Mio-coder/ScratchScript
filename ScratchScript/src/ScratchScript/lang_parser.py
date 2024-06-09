from functools import wraps

from rply import ParserGenerator, Token

from lang_lexer import lang_tokens, lexer
from lang_types import Resource, Event, Assignment, FnCall, MathExpr, Color

pg = ParserGenerator(lang_tokens)


def log_call(fn):
    @wraps(fn)
    def wrapper(p):
        print(
            f"function {fn.__name__} line {fn.__code__.co_firstlineno} got called with "
            f"{len(p)} arg{'s' if len(p) > 1 else ''}: {', '.join(map(str, p))}"
        )
        return fn(p)

    return wrapper


@pg.production('program : statements')
@log_call
def program(p):
    return p[0]


@pg.production('statements : statements statement')
@log_call
def statements(p):
    return p[0] + p[1]


@pg.production('statements : statement')
@log_call
def statements(p):
    return p[0]


@pg.production('statement : resource_stmt')
@pg.production('statement : var_stmt')
@pg.production('statement : code')
def statement(p):
    return [p[0]]


@pg.production('statement : EOL')
def statement(p):
    return []


@pg.production('resource_stmt : NEW ID ID EOL')
@pg.production('resource_stmt : NEW ID ID resource_contents EOL')
@pg.production('resource_stmt : NEW ID ID EQ expr EOL')
@log_call
def resource(p):
    contents = p[3] if len(p) == 5 else None
    init_value = p[4] if len(p) == 6 else None
    return Resource(res_type=p[1].getstr().lower(), name=p[2].getstr(), contents=contents,
                    init_value=init_value)


# syntactic sugar
@pg.production('var_stmt : VAR ID EQ expr EOL')
@pg.production('var_stmt : VAR ID EOL')
def var(p):
    return resource([Token("NEW", "NEW", p[0].getsourcepos())] + p)


@pg.production('resource_contents : L_CURL code R_CURL')
@pg.production('resource_contents : L_PAREN fields R_PAREN')
@log_call
def resource_contents(p):
    return p[1]


@pg.production('event_stmt : ON fn_call L_CURL code R_CURL EOL')
@log_call
def event(p):
    return Event(name=p[1], code=p[3])


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


@pg.production('code_stmt : resource_stmt')
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
    return Assignment(name=p[0], value=p[2])


@pg.production('code_stmt : EOL')
@log_call
def code(p):
    return None


@pg.production('fn_call : attr L_PAREN fn_call_args R_PAREN')
@log_call
def fn_call(p):
    return FnCall(name=p[0], args=p[2])


@pg.production('fn_call : attr L_PAREN R_PAREN')
@log_call
def fn_call(p):
    return FnCall(name=p[0], args=[])


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
        return [p[0].getstr()]
    return p[0] + [p[2].getstr()]


@pg.production('expr : fn_call')
@pg.production('expr : attr')
@pg.production('expr : value')
@pg.production('expr : L_PAREN expr biop expr R_PAREN')
@pg.production('expr : L_PAREN unop expr R_PAREN')
@log_call
def expr(p):
    if len(p) == 1:
        return p[0]
    if len(p) == 3:
        return MathExpr(left=None, op=p[1].getstr(), right=p[2])
    return MathExpr(left=p[1], op=p[2].getstr(), right=p[3])


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


@pg.production('fields : fields field_stmt')
@log_call
def fields(p):
    a, b = p
    a[b[0]] = b[1]
    return a


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
    v = float(p[0].getstr())
    return int(v) if v.is_integer() else v


@pg.production('value : STRING')
@log_call
def value(p):
    return p[0].getstr()


@pg.production('value : COLOR')
@log_call
def value(p):
    return Color(value=p[0].getstr())


@pg.production('value : position')
@log_call
def value(p):
    return p[0]


@pg.production('position : L_PAREN NUMBER COMMA NUMBER R_PAREN')
@log_call
def position(p):
    return float(p[1].getstr()), float(p[3].getstr())


parser = pg.build()


def main(file):
    with open(file) as f:
        source = f.read() + "\n"
    token_stream = lexer.lex(source)
    tokens = list(token_stream)
    # print(print_tokens(tokens))
    result = parser.parse(iter(tokens))
    # try:
    #     result = parser.parse(iter(tokens))
    # except ParsingError as e:
    #     pos: SourcePosition = e.source_pos
    #     msg = f"C:\\Users\\oparm\\PycharmProjects\\PyScratch\\lang\\{file}:{pos.lineno}:{pos.colno}:" \
    #           f" ParsingError: {e.message}"
    #     raise ValueError(msg) from e
    # else:
    #     print(result)


if __name__ == '__main__':
    main("../../example.txt")
