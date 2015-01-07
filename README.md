# The *boxes* module

This module is designed to layout boxes on a page or in a figure. You specify
constraints such as

- This box has an aspect ratio of 3:2.
- The height of this box is the same as that one.
- These four boxes should lie in a grid.
- The complete figure has a width of 12 cm.

and this library will find a set of coordinates that satisfies the constraints.

Here is some example code:

    # TODO

## Requirements

The *boxes* module depends on

- Python 3 (python 2 is not supported, sorry).
- *numpy* (used internally to solve the constraints).

## Using with *matplotlib*

The *boxes* module was written as a more powerfull alternative to the subfigure
support of *matplotlib* and provides some glue code for this usage. Here is an
example

    # TODO

## How it works

The *boxes* module is built on top of `boxes.symmath` which is a library for
cleanly expressing and solving systems of linear equations. `boxes.symmath`
provides a class to represent expressions and this class emulates a numerical
type. *numpy* is used by `boxes.symmath` to do the actual work of solving the
linear systems thus represented.
