import numpy as np
import numpy.linalg
import warnings
from boxes.symmath.expr import Expr


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


def mk_system_(expressions):
  symbols = set()
  expressions = list(expressions)
  for eq in expressions:
    symbols.update(k for k in eq.terms if k != 1)
  symbols = list(symbols)
  a = []
  b = []
  for eq in expressions:
    a.append([eq.terms.get(s, 0) for s in symbols])
    b.append(- eq.terms.get(1, 0))
  return symbols, a, b


def solve(expressions):
  symbols, a, b = mk_system_(expressions)
  if len(expressions) != len(symbols):
    raise RuntimeError(
        'Number of equation must equal number of symbols.'
    )
  x = numpy.linalg.solve(a, b)
  return Solution(zip(symbols, x))


class SymmathWarning(RuntimeWarning):
  pass


def solve_approx(expressions):
  symbols, a, b = mk_system_(expressions)
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
