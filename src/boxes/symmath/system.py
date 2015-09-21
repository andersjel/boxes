from boxes.symmath.expr import Expr
from boxes.symmath.solve import solve, solve_approx
from boxes.namespace import Namespace
from boxes.disjointset import DisjointSet


class System:

  def __init__(self):
    self.set_ = DisjointSet([])

  def equate(self, a, b):
    self.equations.append(Expr(a - b))

  @property
  def equations(self):
    return self.set_.val

  def merge(self, other):
    self.set_.merge(other.set_)

  def solve(self, approx=False):
    if approx:
      sol = solve_approx(self.equations)
    else:
      sol = solve(self.equations)
    return Namespace(sol)
