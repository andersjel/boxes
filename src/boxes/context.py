"""
boxes.context
-------------
"""

import symmath
import boxes.box


class Context:

  def __init__(self):
    self.system = symmath.System()
    self.num_symbols = 0
    self.is_solved = False

  def equate(self, x, y):
    self.system.equate(x, y)

  def solve(self):
    for n in range(self.num_symbols):
      assert n in self.system.facts
    self.is_solved = True

  def sym(self):
    n = self.num_symbols
    self.num_symbols += 1
    return symmath.sym(n)

  def box(self, *args, **kwargs):
    return boxes.box.Box(self, *args, **kwargs)
