from boxes.symmath.expr import Expr
from boxes.symmath.solve import solve, solve_approx
from boxes.merge import MergeList


class System:

  def __init__(self):
    self.equations = MergeList()

  def equate(self, a, b):
    self.equations.append(Expr(a - b))

  def merge(self, other):
    self.equations.merge(other.equations)

  def solve(self, approx=False):
    if approx:
      return solve_approx(self.equations)
    else:
      return solve(self.equations)

  def clear(self):
    self.equations.clear()

  def __str__(self):
    rval = ""
    for expr in self.equations:
      rval += str(expr) + " = 0\n"
    return rval
