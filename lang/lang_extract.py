"""
types:
program -> code=[statements]
statements -> list[statement]
statement -> [
    Empty,
    broadcast_stmt,
    var_stmt,
    sprite_stmt,
]
broadcast_stmt -> name=[str]
var_stmt -> name=[str] (init_value=[Any])?
sprite_stmt -> name=[str]  body=[sprite_content]
sprite_content -> [
    costume_stmt
    sound_stmt
    event_stmt
    code
]
"""
from lang.lang_parser import Node


def parse_main():
