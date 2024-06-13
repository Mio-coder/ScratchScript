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
    Monitor of block ? (need custom logic with var)
    ```
    NEW monitor (
        mode = large
        show = sensing.distanceto(mouse-pointer)
    )
    ```

functions:
how to handle functions with inputs as blocks

raw:
```
motion.goto(TO=motion.goto.menu(TO="_random_"))
```
syntactic sugar:
```
motion.goto(Position::random)
```
```
motion.goto(position.random)
```
```
motion.goto(morion.position.random)
```