import operator


class Expr:

  def __init__(self, other=None, terms=None):
    if terms is not None:
      if other is not None:
        raise ValueError
      self.terms = terms
    elif other is not None:
      if isinstance(other, Expr):
        self.terms = other.terms.copy()
      else:
        # It is a scalar
        self.terms = {1: other}
    else:
      self.terms = {}

  def f_(self, op, other):
    r = Expr(self)
    for k, v in Expr(other).terms.items():
      x = r.terms.get(k, 0)
      r.terms[k] = op(x, v)
    return r

  def __add__(self, other):
    return self.f_(operator.add, other)

  def __sub__(self, other):
    return self.f_(operator.sub, other)

  def __radd__(self, other):
    return self + other

  def __rsub__(self, other):
    return - self + other

  def __neg__(self):
    return self * (-1)

  def __pos__(self):
    return self

  def g_(self, op, other):
    r = Expr(self)
    if isinstance(other, Expr):
      raise RuntimeError
    for k in r.terms:
      r.terms[k] = op(r.terms[k], other)
    return r

  def __mul__(self, other):
    return self.g_(operator.mul, other)

  def __truediv__(self, other):
    return self.g_(operator.truediv, other)

  def __rmul__(self, other):
    return self * other

  def __repr__(self):
    return 'Expr(terms={!r})'.format(self.terms)

  def __str__(self):
    acc = ""

    first = True
    for symbol, val in self.terms.items():
      if val == 0:
        continue

      # Print sign
      if first:
        if val <= 0:
          acc += "−"
      else:
        if val <= 0:
          acc += " − "
        else:
          acc += " + "
      first = False

      has_symbol = symbol != 1

      # Print number and multiplication sign
      if abs(val) != 1:
        acc += str(abs(val))
        if has_symbol:
          acc += "×"

      # Print symbol
      if has_symbol:
        acc += str(symbol)

    return acc


class Unnamed_:
  register = {}
  count = 0

  def __str__(self):
    if self not in Unnamed_.register:
      Unnamed_.register[self] = "s" + str(Unnamed_.count)
      Unnamed_.count += 1
    return Unnamed_.register[self]


def sym(name=None):
  if name is None:
    name = Unnamed_()
  return Expr(terms={name: 1})
