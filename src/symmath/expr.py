import symmath.numerictype
import symmath.format


class Expr(symmath.numerictype.NumericType):

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
    if abs(value) < self.tolerance:
      self.terms.pop(symbol, None)
    else:
      self.terms[symbol] = value

  def substitue(self, symbol, arg):
    coef = self.terms.pop(symbol, 0)
    self += coef * arg

  def scalar(self):
    value = self[None]
    assert self == value
    return value

  def __iadd__(self, other):
    for s, x in Expr(other).terms.items():
      self[s] += x
    return self

  def __imul__(self, val):
    for s in list(self.terms):
      self[s] *= val
    return self

  def __eq__(self, other):
    diff = self - Expr(other)
    return len(diff.terms) == 0

  def __str__(self):
    return symmath.format.format(self.terms.items())

  def __repr__(self):
    return "Expr(" + str(self) + ")"


def sym(name):
  expr = Expr()
  expr[name] = 1
  return expr
