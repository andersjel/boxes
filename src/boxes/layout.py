from boxes.symmath import System
from boxes.merge import MergeList, MergeDict
from collections.abc import Iterable


class Layout:

  def __init__(self):
    self.system = System()
    self.solution = MergeDict()
    self.deferred = MergeList()

  def equate(self, x, y):
    if isinstance(x, Iterable) and isinstance(y, Iterable):
      for x_, y_ in zip(x, y):
        self.equate(x_, y_)
    else:
      self.system.equate(x, y)

  def merge(self, other):
    self.system.merge(other.system)
    self.solution.merge(other.solution)
    self.deferred.merge(other.deferred)

  def solve(self):
    for func in self.deferred:
      func()

    sls = self.system.solve(approx=True)
    self.system.clear()

    self.solution.update(sls)
