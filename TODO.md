# TODO:

Tests:

- tests of block_sb3
    - parse a premade file and compere the result
- ...

Refactor:

- split up block_sb3's load and main
- ...

Features:

- make block_sb3 multi use tool:
    - spec:
        - block-sb3 file -e -f
        - block-sb3 file -f -i
        - e - extract
        - f - make function spec
        - i - extract images
        - ```run(file, extract=True, functions=True)```
        - ```run(file, functions=True, images=True)```
    - goals:
        - move parsing the file from load
        - support more things in parser (bt only relevant in args)
        - add more args
- ...