Grammar features:
  - [ ] Monitors
  - [ ] Lists
  - [ ] In-edtor comments
  - [ ] Full sounds
  - [ ] Full Costumes
  - [ ] Importing
  - [ ] Macros
  - [ ] Procedures 

features spec:
  - Monitors:
    ```
    NEW monitor (
        mode = [str literal]
        show = [function or variable]
    )
    ```
    Monitor of block ? (need custom logic)
    ```
    NEW monitor (
        mode = large
        show = sensing.distanceto(mouse-pointer)
    )
    ```