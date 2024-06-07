```
NEW broadcast test
VAR global_var
NEW sprite A {
    NEW costiume Example_name(
        file = "local_file.svg"
        rotation_centre = (100,50)
    )
    looks.switchcostumeto(Example_name)
    VAR x = 0
    motion.goto(100, 50)
    event.broadcast(test)
    ON event.whenthisspriteclicked() {
          event.broadcast(test)
    }
}
NEW sprite Stage {
    NEW costiume Backdrop1(
        file = "local_file.svg"
        rotation_centre = (100,50)
    )
    NEW costiume Backdrop2(
        file = "local_file.svg"
        rotation_centre = (100,50)
    )
    looks.switchbackdropto(Backdrop1)
    ON event.whenbroadcastreceived(test) {
        looks.switchbackdropto(Backdrop2)
    }
}

resources:
New:
Sprite - curl code
Costiume - fields
Sound - fileds
Broadcast - none
Monitor -
Comment? -

Seperate keyword:
Prototype - 

Create:
Macro
Class?

```
grammar:
```
program: (
      broadcast_stmt
    | var_stmt
    | sprite_stmt
)+
  

sprite_stmt: SPRITE ID L_CURL sprite_content R_CURL EOL

sprite_content: (
      EOL
    | costume_stmt
    | sound_stmt
    | event_stmt
    | code
)+

event_stmt: ON fn_call L_CURL code R_CURL EOL

code: (
      EOL
    | var_stmt
    | fn_call
    | (attr EQ expr EOL)
)+

fn_call: attr L_PAREN (expr (COMMA expr)*)? R_PAREN EOL

attr: ID (DOT ID)*

expr: (
      attr
    | L_PAREN expr biop expr R_PAREN
    | L_PAREN unop expr R_PAREN
    | value
)

biop: ADD | SUB | MUL | DIV | MOD | POW | IN

unop: SUB

costume_stmt: COSTUME ID L_PAREN fields R_PAREN EOL

sound_stmt: SOUND ID L_PAREN fields R_PAREN EOL

fields: field_stmt+

field_stmt: ID EQ value EOL

broadcast_stmt: BROADCAST ID EOL

var_stmt: VAR ID (EQ val)? EOL
value: NUMBER | STRING | COLOR | position

position: L_PAREN NUMBER COMMA NUMBER R_PAREN

ID: [\w_][\w\d_]*
NUMBER: \d+(\.\d+)?
STRING: "([^"\\]|(\\[\\"nt]))+"
COLOR: #[0-9a-zA-Z]{6}

EOL: \n
BROADCAST: "broadcast"
VAR: "var"
SPRITE: "sprite"
COSTUME: "costume"
SOUND: "sound"
ON: "on"
EQ: "="
DOT: "\."
COMMA: ","

ADD: "\+"
SUB: "-"
MUL: "\*"
DIV: "/"
MOD: "%"
POW: "\*\*"
IN: "in"

L_CURL: "{"
R_CURL: "}"
L_PAREN: "\("
R_PAREN: "\)"
```