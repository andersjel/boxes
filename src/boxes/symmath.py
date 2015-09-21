import numpy as np
import numpy.linalg
import operator
import warnings


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


class Solution(dict):

  def eval(self, expr):
    if isinstance(expr, tuple):
      return tuple(self.eval(x) for x in expr)
    elif isinstance(expr, list):
      return [self.eval(x) for x in expr]
    expr = Expr(expr)
    val = 0
    for k, v in expr.terms.items():
      if k == 1:
        val += v
      else:
        val += self[k] * v
    return val


def mk_system(equations):
  symbols = set()
  equations = list(equations)
  for eq in equations:
    symbols.update(k for k in eq.terms if k != 1)
  symbols = list(symbols)
  a = []
  b = []
  for eq in equations:
    a.append([eq.terms.get(s, 0) for s in symbols])
    b.append(- eq.terms.get(1, 0))
  return symbols, a, b


def solve(equations):
  symbols, a, b = mk_system(equations)
  if len(equations) != len(symbols):
    raise RuntimeError(
        'Number of equation must equal number of symbols.'
    )
  x = numpy.linalg.solve(a, b)
  return Solution(zip(symbols, x))


class SymmathWarning(RuntimeWarning):
  pass


def solve_harder(equations):
  symbols, a, b = mk_system(equations)
  sol = numpy.linalg.lstsq(a, b)
  x, residuals, rank, _ = sol
  if rank != len(symbols):
    warnings.warn(
        'Rank of system ({}) does not match number of symbols ({}).'
        .format(rank, len(symbols)), SymmathWarning
    )
  if residuals > 1e-15:
    warnings.warn('System is over-constrained', SymmathWarning)
  return Solution(zip(symbols, sol[0]))


class Namespace:

  def __init__(self, content):
    self.__dict__.update(content)
    self._content = content

  def __repr__(self):
    return 'Namespace({!r})'.format(self._content)
