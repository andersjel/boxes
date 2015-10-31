"""
boxes
-----

Convenience reexports. Typing ``from boxes import *`` imports the following:

* The class :class:`boxes.box.Box` which is the principal class of the library.
* The module :mod:`boxes.constrain` which contains a bunch of convenient
  constraints.
* The functions :func:`symmath.sym` and :func:`boxes.box.context` which are
  all that is needed to create custom constraints.

"""
from boxes.context import Context
from boxes import constrain

__all__ = ['Context', 'constrain']
