"""
Module: boxes.cartesian
-----------------------
"""

from collections import namedtuple


class Vect(namedtuple('Vect', 'x y')):

  def __add__(self, other):
    return Vect(u + v for u, v in zip(self, other))

  def __sub__(self, other):
    return Vect(u - v for u, v in zip(self, other))


class Rect(namedtuple('Rect', 'top right bottom left')):
  @property
  def width(self):
    return self.right - self.left

  @property
  def height(self):
    return self.bottom - self.top

  @property
  def loc(self):
    return Vect(self.left, self.top)

  @property
  def size(self):
    return Vect(self.width, self.height)
