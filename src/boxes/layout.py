from boxes.symmath import System
from boxes.mergelist import MergeList


class Layout:

  def __init__(self):
    self.system = System()
    self.boxes = MergeList()
    self.page = Box(self)

  def equate(self, x, y):
    self.system.equate(x, y)

  def merge(self, other):
    self.system.merge(other.system)
    self.boxes.merge(other.boxes)
