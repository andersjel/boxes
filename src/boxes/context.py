"""
boxes.context
-------------

.. autoclass:: Context()
  :members:
"""

import symmath
import boxes.box


class Context:
  """

    .. attribute:: system

      The underlying :class:`~symmath.system.System` holding all equations
      constraining the layout.

    .. attribute:: is_solved

      A :class:`bool` indicating whether :func:`solve` has been called.

  """

  def __init__(self):
    self.system = symmath.System()
    self.num_symbols = 0
    self.is_solved = False

  def equate(self, x, y):
    """
      Add a constraint setting *x == y*.
    """
    self.system.equate(x, y)

  def solve(self):
    """

      Solve the layout. This function raises an error if the layout is not fully
      defined.

    """
    for n in range(self.num_symbols):
      assert n in self.system.facts
    self.is_solved = True

  def sym(self):
    """

      Create an expression (of type :class:`symmath.expr.Expr`) representing a
      fresh symbol unused in this context.

    """
    n = self.num_symbols
    self.num_symbols += 1
    return symmath.sym(n)

  def box(self, *args, **kwargs):
    """
      Construct a :class:`~boxes.box.Box` using this context.
    """
    return boxes.box.Box(self, *args, **kwargs)
