import numpy as np
import numpy.linalg
import warnings
from boxes.symmath.expr import Expr


def substitute(solution, expr, partial=False):
  if isinstance(expr, tuple) or isinstance(expr, list):
    if hasattr(expr, '_make'):
      # This is a named tuple
      return expr.__class__._make(substitute(solution, x) for x in expr)
    return expr.__class__(substitute(solution, x) for x in expr)
  expr = Expr(expr)
  val = 0
  for k, v in expr.terms.items():
    if k == 1:
      val += v
    else:
      try:
        val += solution[k] * v
      except KeyError:
        if partial:
          val += Expr(terms={k: v})
        else:
          raise
  return val


def _mk_system(expressions):
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
  symbols, a, b = _mk_system(expressions)
  if len(expressions) != len(symbols):
    raise RuntimeError(
        'Number of equation must equal number of symbols.'
    )
  x = numpy.linalg.solve(a, b)
  return dict(zip(symbols, x))


class SymmathWarning(RuntimeWarning):
  pass


def solve_approx(expressions):
  symbols, a, b = _mk_system(expressions)
  sol = numpy.linalg.lstsq(a, b)
  x, residuals, rank, _ = sol
  if rank != len(symbols):
    warnings.warn(
        'Rank of system ({}) does not match number of symbols ({}).'
        .format(rank, len(symbols)), SymmathWarning
    )
  if residuals > 1e-15:
    warnings.warn('System is over-constrained', SymmathWarning)
  return dict(zip(symbols, sol[0]))
