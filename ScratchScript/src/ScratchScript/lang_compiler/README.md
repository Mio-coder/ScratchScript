## Files
  - lang_code.py:
    - parse_code - main fn 
    - Parser Data -> Compiler Data
    - statements to list of function call objects
  - lang_extract.py:
    - parse_program - main fn:
      - parse the whole data from parser
    - handles sprites and variables
    - it will handle Costumes and sounds
  - lang_functions.py:
    - function call objects
    - creates an object that returns a PyScratch Object
    - lang_types.py:
      - types for all the lang_extract.py stuff
      - extracted form lang_extract.py because sprites can be arguments

lang_code - parse code
lang_functions - ABC for functions
lang_extract - main
lang_types - types

## TODO:
 - [x] rewrite lang_code.parse_fn_call
 - [ ] make lang_code.parse_expr
 - [ ] rethink parsing fn calls
 - [x] does we need specs in lang_functions? No