Grammar features:
  - [ ] Monitors
  - [ ] Lists
  - [ ] In-edtor comments
  - [ ] Full sounds
  - [ ] Full Costumes
  - [ ] Importing
  - [ ] AST-macros
  - [ ] Procedures 

features spec:
  - Monitors:
    ```
    MONITOR (
        mode = [str literal]
        show = [function or variable]
    )
    ```
    Monitor of block
    ```
    MONITOR (
        mode = large
        show = sensing.distanceto(mouse-pointer)
    )
    ```