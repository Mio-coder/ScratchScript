BROADCAST:broadcast  ID:test EOL:\n
VAR:var  ID:global_var EOL:\n
SPRITE:sprite  ID:A  L_CURL:{ EOL:\n
    COSTUME:costume  ID:Example_name L_PAREN:( EOL:\n
        ID:file  EQ:=  STRING:"local_file.svg" EOL:\n
        ID:rotation_centre  EQ:=  L_PAREN:( NUMBER:100 COMMA:, NUMBER:50 R_PAREN:) EOL:\n
    R_PAREN:) EOL:\n
    ID:looks DOT:. ID:switchcostumeto L_PAREN:( ID:Example_name R_PAREN:) EOL:\n
    VAR:var  ID:x  EQ:=  NUMBER:0 EOL:\n
    ID:motion DOT:. ID:goto L_PAREN:( NUMBER:100 COMMA:,  NUMBER:50 R_PAREN:) EOL:\n
    ON:on  ID:event DOT:. ID:whenthisspriteclicked  L_CURL:{ EOL:\n
        ID:event DOT:. BROADCAST:broadcast L_PAREN:( ID:test R_PAREN:) EOL:\n
    R_CURL:} EOL:\n
R_CURL:} EOL:\n
SPRITE:sprite  ID:Stage  L_CURL:{ EOL:\n
    COSTUME:costume  ID:Backdrop1 L_PAREN:( EOL:\n
        ID:file  EQ:=  STRING:"local_file.svg" EOL:\n
        ID:rotation_centre  EQ:=  L_PAREN:( NUMBER:100 COMMA:, NUMBER:50 R_PAREN:) EOL:\n
    R_PAREN:) EOL:\n
    COSTUME:costume  ID:Backdrop2 L_PAREN:( EOL:\n
        ID:file  EQ:=  STRING:"local_file.svg" EOL:\n
        ID:rotation_centre  EQ:=  L_PAREN:( NUMBER:100 COMMA:, NUMBER:50 R_PAREN:) EOL:\n
    R_PAREN:) EOL:\n
    ID:looks DOT:. ID:switchbackdropto L_PAREN:( ID:Backdrop1 R_PAREN:) EOL:\n
    ON:on  ID:event DOT:. ID:whenbroadcastreceived L_PAREN:( ID:test R_PAREN:)  L_CURL:{ EOL:\n
        ID:looks DOT:. ID:switchbackdropto L_PAREN:( ID:Backdrop2 R_PAREN:) EOL:\n
    R_CURL:} EOL:\n
R_CURL:} EOL:\n