"""
boxes
-----

Convenience reexports. Typing ``from boxes import *`` imports the following:

* The class :class:`boxes.box.Box` which is the principal class of the library.
* The module :mod:`boxes.constrain` which contains a bunch of convenient
  constraints.
* The functions :func:`symmath.sym` and :func:`boxes.box.entangle` which are
  all that is needed to create custom constraints.

"""
from boxes.box import Box, entangle
from symmath import sym
from boxes import constrain

__all__ = ['Box', 'constrain', 'sym', 'entangle']
