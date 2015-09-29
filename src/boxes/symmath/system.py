from boxes.symmath.expr import Expr
from boxes.symmath.solve import solve, solve_approx
from boxes.mergelist import MergeList


class System:

  def __init__(self):
    self.equations = MergeList()

  def equate(self, a, b):
    self.equations.append(Expr(a - b))

  def merge(self, other):
    self.equations.merge(other.equations)

  def solve(self, approx=False):
    if approx:
      sol = solve_approx(self.equations)
    else:
      sol = solve(self.equations)
    return sol

  def clear(self):
    self.equations.clear()
