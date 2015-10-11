"""
boxes.layout
------------
"""

from symmath import System
from symmath.merge import MergeDict
from collections.abc import Iterable


class Layout:

  def __init__(self):
    self.system = System()
    self.solution = MergeDict()

  def equate(self, x, y):
    if isinstance(x, Iterable) and isinstance(y, Iterable):
      for x_, y_ in zip(x, y):
        self.equate(x_, y_)
    else:
      self.system.equate(x, y)

  def merge(self, other):
    self.system.merge(other.system)
    self.solution.merge(other.solution)

  def solve(self):
    sls = self.system.solve(approx=True)
    self.system.clear()
    self.solution.update(sls)
