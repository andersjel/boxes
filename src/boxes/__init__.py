"""
boxes
-----

Convenience reexports. Typing ``from boxes import *`` imports the following:

* The class :class:`boxes.box.Context` which which you need to instance to use
  the library.
* The module :mod:`boxes.constrain` which contains a bunch of convenient
  constraints.

"""
from boxes.context import Context
from boxes import constrain

__all__ = ['Context', 'constrain']
