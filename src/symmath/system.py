"""
symmath.system
--------------

.. doctest::
  :hide:

  >>> from symmath import *

.. autoclass:: System
  :members:
  :undoc-members:

  .. attribute:: facts

    A dictionary mapping symbol names to equivalent expressions. Each value in
    this dictionary should not contain any references to the symbols used as
    keys. Consider this attribute read-only, and use :func:`equate` to add a
    fact instead of modifying this dictionary.

"""
from symmath.expr import Expr
from collections import abc


class System:

  def __init__(self):
    self.facts = {}

  def rewrite(self, expr):
    """
    Substitue all known :attr:`facts` into *expr*.
    """
    for symbol in list(expr.terms):
      try:
        fact = self.facts[symbol]
      except KeyError:
        continue
      expr.substitue(symbol, fact)

  def simplify(self, expr):
    """

    Same as :func:`rewrite`, but returns the simplified expression instead of
    modifying *expr*.

    """
    expr = Expr(expr)
    self.rewrite(expr)
    return expr

  def eval(self, val):
    """

    Substitue all known facts into *val*, recursing into structures that support
    it. :func:`eval` calls :func:`symmath.expr.Expr.scalar` to eliminate all
    expressions. This method raises an exception if the system is not fully
    solved.

    Classes supporting this function define the method :func:`_symmath_eval`,
    which takes a single argument: the :func:`eval` method as a bound method,
    and should return a fully evaluated copy of itself.

    """
    if hasattr(val, '_symmath_eval'):
      return val._symmath_eval(self.eval)
    return self.simplify(val).scalar()

  def equate(self, a, b):
    """

    Eliminate one symbol from the system by using the equation: *a = b*.
    This adds a fact to :attr:`facts` and simplifies all existing facts.

    Classes can define :func:`_symmath_equate` to customize what it means
    objects of that class to be equal to something else.

    .. doctest::

      >>> class Vector2D:
      ...   def __init__(self, x, y):
      ...     self.x = x
      ...     self.y = y
      ...
      ...   def _symmath_equate(self, f, other):
      ...     f(self.x, other.x)
      ...     f(self.y, other.y)

      >>> x = sym('x')
      >>> y = sym('y')
      >>> a = Vector2D(x + 5, 2*y)
      >>> b = Vector2D(4*y, 3*x)

      >>> system = System()
      >>> system.equate(a, b)
      >>> system.eval(x)
      1.0
      >>> system.eval(y)
      1.5

    """
    if hasattr(a, '_symmath_equate'):
      a._symmath_equate(self.equate, b)
      return
    if hasattr(b, '_symmath_equate'):
      b._symmath_equate(self.equate, a)
      return
    if isinstance(a, abc.Iterable) and isinstance(b, abc.Iterable):
      for x, y in zip(a, b):
        self.equate(x, y)
      return
    expr = self.simplify(a - b)
    if expr == 0:
      return
    # We now have an equation
    #
    #   0 = c_1 x_1 + c_2 x_2 + ...
    #
    # where {x_1, x_2, ... } are symbols. We find the pair (x_i, c_i) where c_i
    # is maximal, as this will lead to the smallest round-off errors later.
    symbol, coef = max(
        ((k, v) for k, v in expr.terms.items() if k is not None),
        key=lambda x: x[1]
    )
    # We now rearrange x_i = (c_1 x_1 + c_2 x_2 + ...) / c_i
    expr[symbol] = 0
    expr /= - coef
    # and substitue this into all the old facts to eliminate x_i.
    for subs in self.facts.values():
      subs.substitue(symbol, expr)
    # finally add x_i as a fact
    self.facts[symbol] = expr
