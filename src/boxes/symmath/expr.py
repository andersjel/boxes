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


def sym(name=None):
  if name is None:
    name = object()
  return Expr(terms={name: 1})
