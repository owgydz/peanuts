# Peanuts Language Syntax

Docs Version: 100.25

Peanut Version: 1.0.2_r6



---

## Overview

Peanuts is an indentation-based programming language inspired by Python, with playful keyword naming and a clean execution model.

Peanuts source files use the `.nut` extension.

Example:

```peanuts
nut main():
    print("Hello, Peanuts!")

main()
```

## File Structure

A Peanuts program consists of:

- Top-level statements

- Function definitions

- Imports

- Executed expressions

There is no required entrypoint, but using a main() function is recommended.

## Indentation

Peanuts uses indentation to define blocks, similar to Python.

Rules:

Use consistent indentation (spaces recommended).

Indentation defines scope for:

- Functions

- Conditionals

- Loops


Example:

```nut main():
    jar x = 5
    crunch x > 3:
        print("x is large")
```
## Comments

Single-line comments:

```# This is a comment
jar x = 10  # Inline comment
```

NOTE: Multi-line comments are not currently supported.

## Variables

Variables are declared using the jar keyword.
```
jar x = 5
jar name = "Peanut"
jar flag = true
```

- Variables are dynamically typed.

## Literals
Numbers
```
jar a = 10
jar b = 42
```
***(Only integers are guaranteed in 1.0.2_r4.)***

## Strings

Peanuts supports both double and single quotes:
```
jar a = "hello"
jar b = 'world'
# booleans
jar a = true
jar b = false
```
Booleans map to Python's True and False.

## Functions

Functions are declared using `nut`.

```
nut add(a, b):
    spread a + b
```
### Calling a function:
```
jar result = add(5, 3)
```
## Return Values

Use spread to return a value.
```
nut square(x):
    spread x * x
```
If no spread is used, the function returns nothing.

# Control Flow
## Conditionals

Use crunch for if.
```
crunch x > 5:
    print("Greater")
otherwise:
    print("Smaller or equal")
```
`otherwise` acts as else.

## Loops

Use chew for for.

`chew item in items:
    print(item)
`
- Operators
- Arithmetic
- `+`   addition
- `-`   subtraction
- `*`   multiplication
- `/`   division

### Example:

`jar x = 10 + 5 * 2`
Comparison
`== `  equal
`!=`   not equal
`>`    greater than
`<`    less than
Logical
`and`
`or`
`not`

Example:

```crunch x > 5 and not flag:
    print("Condition met")
```
## Unary Expressions

Peanuts supports unary operators:
```
jar x = -5
jar y = not true
```
## Member Access

Use dot notation:

`import nutmath`

`jar result = nutmath.add(5, 3)`

### Imports

Basic import:

`import nutmath`

This loads a module and assigns it to a variable of the same name.

Module resolution order:

Current directory

Standard library

Installed packages

## Expressions as Statements

Expressions can be written directly:
```
add(1, 2)
print("Done")
```
## Standard Library

Peanuts ships with built-in modules:

`nutmath`

`nutstr`

`nutio`

`nuttime`

`nutrand`

`nutfs`

Example:
```
import nutrand

jar x = nutrand.randint(1, 10)
```

## Execution Model

Peanuts:

Lexes source code

Builds an AST

Transpiles to Python

Executes in a controlled runtime environment

Runtime errors are formatted and reported with file and line context.