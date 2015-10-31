# The *boxes* library

This Python 3 library is designed to layout boxes on a page or in a figure. You
specify constraints such as

- This box has an aspect ratio of 3:2.
- The height of this box is the same as that one.
- These four boxes should lie in a grid.
- The complete figure has a width of 12 cm.

and this library will find a set of coordinates that satisfies the constraints.

## The *symmath* package

The *boxes* library builts on top of the included *symmath* package which is a
library for cleanly expressing and solving systems of linear equations. Any
constraint which can be expressed as a set of linear equations can be
implemented in this way.
