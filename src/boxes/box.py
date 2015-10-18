"""
boxes.box
---------

.. autosummary::
  Box
  entangle

.. autoclass:: Box

  .. rubric:: Methods

  .. automethod:: solve
  .. automethod:: fix
  .. automethod:: pad
  .. automethod:: surround

  .. rubric:: Properties

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

    Represents a rectangle in the layout. The position of the rectangle is given
    by the :attr:`rect` property.

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

      Construct a new box similar to this, but smaller by the given amount.

      The method can be called in four different ways (similar to how margins
      and padding is specified in *css* files):

      * :samp:`box.pad({all})`
      * :samp:`box.pad({vert}, {hor})`
      * :samp:`box.pad({top}, {hor}, {bottom})`
      * :samp:`box.pad({top}, {right}, {bottom}, {left})`

      .. rubric:: Simple example

      .. doctest::

        >>> from boxes import *
        >>> outer_box = Box(width=10)
        >>> inner_box = Box(height=4)
        >>> outer_box.pad(0.5).fix(inner_box)
        >>> outer_box.solve()
        >>> print(outer_box.loc, outer_box.size)
        (0.0, 0.0) (10.0, 5.0)
        >>> print(inner_box.loc, inner_box.size)
        (0.5, 0.5) (9.0, 4.0)

      .. rubric:: Center a box inside another

      .. doctest::

        >>> from boxes import *
        >>> outer_box = Box(size=(6, 5))
        >>> inner_box = Box(size=(4, 4))
        >>> outer_box.pad(sym(), sym()).fix(inner_box)
        >>> outer_box.solve()
        >>> print(outer_box.loc, outer_box.size)
        (0.0, 0.0) (6.0, 5.0)
        >>> print(inner_box.loc, inner_box.size)
        (1.0, 0.5) (4.0, 4.0)
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

      Similar to :func:`pad`, but the arguments are negated.

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


def entangle(*boxes):
  """

    Combines the layout of several boxes.

    This function uses :func:`boxes.layout.Layout.merge` to combine the layout
    of each box in *boxes* and returns the resulting layout. This has the effect
    of informing the library that the equations defining the boxes are
    intertwined and need to be solved together.

    You rarely need to call this function directly, but it is needed when making
    custom constraints. Here is an example setting the width of ``box_1`` to
    twice the width of ``box_2``.

    .. doctest::

      >>> from boxes import *
      >>> box_1 = Box()
      >>> box_2 = Box()
      >>> layout = entangle(box_1, box_2)
      >>> layout.equate(box_1.width, 2 * box_2.width)
      >>> figure = Box(size=(10, 5))
      >>> figure.fix(constrain.row(box_1, box_2, spacing=1.0))
      >>> figure.solve()
      >>> print(box_1.width)
      6.0
      >>> print(box_2.width)
      3.0

    Technically, the call to :func:`boxes.constrain.row` will also entangle the
    two boxes, so the call to entangle is superfluous here. A good rule is: When
    manually adding a constraint involving more than one box, :func:`entangle`
    should be called (instead of grabbing the :attr:`layout` property of one of
    the boxes).

  """
  layout = boxes[0].layout
  for r in boxes[1:]:
    layout.merge(r.layout)
  return layout
