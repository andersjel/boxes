from boxes.symmath import System
from boxes.mergelist import MergeList
from collections.abc import Iterable


class Layout:

  def __init__(self):
    self.system = System()
    self.boxes = MergeList()
    self.deferred = MergeList()

  def equate(self, x, y):
    if isinstance(x, Iterable) and isinstance(y, Iterable):
      for x_, y_ in zip(x, y):
        self.equate(x_, y_)
    else:
      self.system.equate(x, y)

  def merge(self, other):
    self.system.merge(other.system)
    self.boxes.merge(other.boxes)
    self.deferred.merge(other.deferred)

  def solve(self):
    for func in self.deferred:
      func()

    sls = self.system.solve(approx=True)
    self.system.clear()

    for b in self.boxes:
      b.update(sls)

    return sls
