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

  def _symmath_substitute(self, f):
    return Vect(f(x) for x in self)

  def _symmath_equate(self, other):
    return zip(self, other)

  def __str__(self):
    def rounded():
      for x in self:
        try:
          # Round and add zero to remove negative zeros.
          yield round(float(x), 6) + 0
        except:
          yield x
    return "({}, {})".format(*rounded())


class Rect:
  def __init__(self, top, right, bottom, left):
    self.top = top
    self.right = right
    self.bottom = bottom
    self.left = left
    self.width = right - left
    self.height = bottom - top
    self.loc = Vect(left, top)
    self.size = Vect(self.width, self.height)

  def _symmath_substitute(self, f):
    return Rect(
        f(self.top),
        f(self.right),
        f(self.bottom),
        f(self.left),
    )

  def _symmath_equate(self, other):
    yield self.top, other.top
    yield self.right, other.right
    yield self.bottom, other.bottom
    yield self.left, other.left
