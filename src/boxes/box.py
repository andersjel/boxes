"""
Module: boxes.box
-----------------

.. autoclass:: Box

  **Methods:**

  .. automethod:: solve
  .. automethod:: fix
  .. automethod:: pad
  .. automethod:: surround

  **Properties:**

  .. autoattribute:: rect
  .. attribute:: width, height, top, right, bottom, left, loc, and size

    Any property of :attr:`rect` is also made a property of this class.

  .. attribute:: layout

    The :class:`boxes.layout.Layout` of this box. You rarely need to access this
    directly (use :func:`entangle` instead).

.. autofunction:: entangle

"""

from boxes.cartesian import Vect, Rect
from boxes.layout import Layout
from symmath import sym, substitute
import itertools


class Box:
  """

    A rectangle in the layout. The position of the rectangle is given by the
    :attr:`rect` property.

    All arguments to the constructor are optional, and the same effect can be
    obtained by later constraining the box.

    :arg boxes.cartesian.Rect rect:
      Explicitly locate the box.
    :arg boxes.layout.Layout layout:
      Explicitly set the layout of the box.
    :arg float aspect:
      Forwarded to :func:`boxes.constrain.aspect`.

    In addition, any property of :class:`~boxes.cartesian.Rect` can be used as a
    keyword argument to the constructor, which will introduce a constraint.

  """

  _rect_attrs = set('width height top right bottom left loc size'.split())

  def __init__(self, rect=None, layout=None, aspect=None, **kwargs):
    self.layout = layout if layout else Layout()
    self._rect = rect if rect else Rect(sym(), sym(), sym(), sym())

    for k, v in kwargs.items():
      if k in self._rect_attrs:
        if v is not None:
          self.layout.equate(getattr(self.rect, k), v)
        else:
          raise TypeError(
              "Box(...) got an unexpected keyword argument: {}"
              .format(repr(k))
          )

    if aspect is not None:
      import boxes.constrain
      boxes.constrain.aspect(aspect, self)

  @property
  def rect(self):
    """

      The position of the box as a :class:`boxes.cartesian.Rect` instance. The
      dimensions of *rect* are expressions of type :class:`symmath.expr.Expr`
      until you :func:`solve` the layout.

    """
    return substitute(self.layout.solution, self._rect, partial=True)

  def solve(self, fix_upper_left=True):
    """

    Solves the associated :attr:`layout`. After calling this method, this box
    and all boxes entangled with it will have concrete values for their
    dimensions instead of symbolic expressions.

    :arg bool fix_upper_left:

      If :const:`True` (which is the default) constrain ``self.loc`` to ``(0,
      0)`` before solving the layout.

    """
    if fix_upper_left:
      self.layout.equate(self.loc, Vect(0, 0))
    return self.layout.solve()

  def fix(self, other):
    """Constrain this box and *other* to have the same size and position."""
    layout = entangle(self, other)
    layout.equate(self.rect, other.rect)

  def pad(self, *args):
    """

      Construct a new box by...

    """
    if len(args) > 4:
      raise TypeError(
          'Box.pad(..) takes at most 4 arguments ({} was given).'
          .format(len(args))
      )
    top, right, bottom, left = itertools.islice(itertools.cycle(args), 4)
    rect = Rect(
      top=self.rect.top + top,
      right=self.rect.right - right,
      bottom=self.rect.bottom - bottom,
      left=self.rect.left + left,
    )
    return Box(layout=self.layout, rect=rect)

  def surround(self, *args):
    """

      Similar to :func:`pad`, but ...

    """
    return self.pad(*(-x for x in args))


def _add_attr(attr):
  def getter(self):
    return getattr(self.rect, attr)

  getter.__name__ = attr
  setattr(Box, attr, property(getter))


for attr in Box._rect_attrs:
  _add_attr(attr)
del attr
del _add_attr


def entangle(*bs):
  layout = bs[0].layout
  for r in bs[1:]:
    layout.merge(r.layout)
  return layout
