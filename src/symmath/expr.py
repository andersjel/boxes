"""
symmath.expr
------------

.. doctest::
  :hide:

  >>> from symmath import *

.. autoexception:: SymmathError
  :show-inheritance:

.. autoclass:: Expr
  :members:
  :undoc-members:

.. autofunction:: sym
"""
import symmath.numerictype
import symmath.format


class SymmathError(ValueError):
  pass


class Expr(symmath.numerictype.NumericType):
  """

  Class used for symbolic computations. :doc:`/symmath-intro` describes what
  operations this class supports.

  .. attribute:: terms

    A mapping from symbol names to their coefficients.

  .. attribute:: tolerance

    Numbers smaller than the *tolerance* in absolute value are converted to 0.
  """

  def __init__(self, other=None, tolerance=1e-8):
    if isinstance(other, Expr):
      self.terms = other.terms.copy()
      self.tolerance = other.tolerance
    else:
      self.terms = {}
      self.tolerance = tolerance
      if other is not None:
        self[None] = other

  def __getitem__(self, symbol):
    try:
      return self.terms[symbol]
    except KeyError:
      return 0

  def __setitem__(self, symbol, value):
    if abs(value) <= self.tolerance:
      self.terms.pop(symbol, None)
    else:
      self.terms[symbol] = value

  def __delitem__(self, symbol):
    self[symbol] = 0

  def substitue(self, symbol, arg):
    """

    Replace all occurances of *symbol* with *arg*.

    >>> from symmath import sym
    >>> x = sym("x")
    >>> y = sym("y")
    >>> z = sym("z")
    >>> e = 2 * x + y + 1
    >>> e.substitue("x", y + z)
    >>> print(e)
    3 y + 2 z + 1
    """
    coef = self.terms.pop(symbol, 0)
    self += coef * arg

  def scalar(self):
    """

    If *x* contains no symbols, ``x.scalar()`` returns a regular float equal to
    the scalar part of *x*. Otherwise an exception is raised.

    >>> a = sym('a')
    >>> x = a + 3
    >>> x.scalar()
    Traceback (most recent call last):
      ...
    SymmathError: Not a scalar
    >>> x -= a
    >>> x
    Expr(3)
    >>> x.scalar()
    3

    """
    value = self[None]
    if self != value:
      raise SymmathError('Not a scalar')
    return value

  def __iadd__(self, other):
    for s, x in Expr(other).terms.items():
      self[s] += x
    return self

  def __imul__(self, val):
    if isinstance(val, Expr):
      raise SymmathError('Symmath expressions cannot be multiplied together')
    for s in list(self.terms):
      self[s] *= val
    return self

  def __eq__(self, other):
    diff = self - Expr(other)
    return len(diff.terms) == 0

  def __str__(self):
    return symmath.format.format(self)

  def __repr__(self):
    return "Expr(" + str(self) + ")"


def sym(symbol):
  """
  Create an expression containing just the given symbol.

  >>> sym('a')
  Expr(a)
  """
  expr = Expr()
  expr[symbol] = 1
  return expr
