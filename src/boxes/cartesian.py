"""
boxes.cartesian
---------------

.. autosummary::
  Vect
  Rect

.. autoclass:: Vect(x, y)
.. autoclass:: Rect

"""

from collections import namedtuple


class Vect(namedtuple('Vect', 'x y')):
  """
    Class of two-dimensional vectors.

    This a named tuple (see :func:`collections.namedtuple` from the python
    standard library) with an :attr:`x` and a :attr:`y` attribute. Implements
    :func:`__add__` and :func:`__sub__`.

  """

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
  """
    Holds the dimensions of a rectangle.

    Objects of this class cannot be modified after creation

    >>> from boxes.cartesian import Rect
    >>> r = Rect(0, 1, 1, 0)
    >>> r.right = 2
    Traceback (most recent call last):
      ...
    TypeError: 'Rect' objects are immutable

    .. attribute:: top

      The *y*-coordinate of the top edge of the rectangle.

    .. attribute:: right

      The *x*-coordinate of the right edge of the rectangle.

    .. attribute:: bottom

      The *y*-coordinate of the bottom edge of the rectangle.

    .. attribute:: left

      The *x*-coordinate of the left edge of the rectangle.

    .. attribute:: width

      The width of the rectangle.

    .. attribute:: height

      The height of the rectangle.

    .. attribute:: loc

      The upper left corner of the rectangle (as a :class:`Vect`).

    .. attribute:: size

      The size of the rectangle (as a :class:`Vect`).

  """

  def __init__(self, top, right, bottom, left):
    width = right - left
    height = bottom - top
    self.__dict__.update(
        top=top, right=right, bottom=bottom, left=left,
        width=width, height=height,
        loc=Vect(left, top),
        size=Vect(width, height),
    )

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

  def __setattr__(self, attr, val):
    raise TypeError("'Rect' objects are immutable")
