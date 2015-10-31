"""
boxes.constrain
---------------

.. autosummary::
  align
  row
  column
  hcat
  vcat
  aspect
  width
  height
  size

"""

from boxes.cartesian import Vect, Rect
from boxes.box import Box


__all__ = []


def public(f):
  __all__.append(f.__name__)
  return f


_edges = {
    't': 'top',
    'b': 'bottom',
    'l': 'left',
    'r': 'right',
}


@public
def align(edges, *boxes):
  """
    Aligns boxes along the specified edges.

    This function adds contraints aligning the given boxes along edges specified
    in the following manner:

    * If ``'t'`` is in *edges*, equate the *y*-coordinates of the top edges of
      every box in *boxes*.
    * If ``'r'`` is in *edges*, equate the *x*-coordinates of the right edges of
      every box in *boxes*.
    * If ``'b'`` is in *edges*, equate the *y*-coordinates of the bottom edges
      of every box in *boxes*.
    * If ``'l'`` is in *edges*, equate the *x*-coordinates of the left edges of
      every box in *boxes*.

    :arg str edges:
      Any combination of the letters ``'t'``, ``'r'``, ``'b'``, and ``'l'``.
    :arg boxes:
      An iterable over the :class:`~boxes.box.Box` objects to align.

  """
  a = boxes[0]
  for b in boxes[1:]:
    for e in edges:
      a.context.equate(getattr(a, _edges[e]), getattr(b, _edges[e]))


@public
def row(*boxes, spacing=0):
  """

    Place the given boxes along a horizontal row with the given *spacing*
    between them. The boxes will align along the top and bottom edges.

    :arg boxes:
      An iterable over the :class:`~boxes.box.Box` objects to put in a row.
    :arg spacing:
      The spacing between the boxes (this can be a :class:`float` or an
      :class:`~symmath.expr.Expr`).

  """
  hcat(*boxes, spacing=spacing)
  align("tb", *boxes)
  return _bbox(boxes)


@public
def column(*boxes, spacing=0):
  """

    Place the given boxes along a vertical column with the given *spacing*
    between them. The boxes will align along the left and right edges.

    :arg boxes:
      An iterable over the :class:`~boxes.box.Box` objects to put in a column.
    :arg spacing:
      The spacing between the boxes (this can be a :class:`float` or an
      :class:`~symmath.expr.Expr`).

  """
  vcat(*boxes, spacing=spacing)
  align("lr", *boxes)
  return _bbox(boxes)


@public
def hcat(*boxes, spacing=0):
  """

    Similar to :func:`column` but does not constrain top and bottom edges in any
    way.

    :arg boxes:
      An iterable over :class:`~boxes.box.Box` objects.
    :arg spacing:
      The spacing between the boxes (this can be a :class:`float` or an
      :class:`~symmath.expr.Expr`).

  """
  for a, b in _pairs(boxes):
    a.context.equate(a.right + spacing, b.left)


@public
def vcat(*boxes, spacing=0):
  """

    Similar to :func:`row` but does not constrain left and right edges in any
    way.

    :arg boxes:
      An iterable over :class:`~boxes.box.Box` objects.
    :arg spacing:
      The spacing between the boxes (this can be a :class:`float` or an
      :class:`~symmath.expr.Expr`).

  """
  for a, b in _pairs(boxes):
    a.context.equate(a.bottom + spacing, b.top)


@public
def aspect(aspect, *boxes):
  """

    Constrain every box in *boxes* to have the given aspect ratio.

    :arg float aspect:
      The aspect ratio is defined as the width divided by the height.
    :arg boxes:
      An iterable over :class:`~boxes.box.Box` objects.

  """
  for box in boxes:
    box.context.equate(box.width, box.height * aspect)


@public
def width(width, *boxes):
  """

    Constrain the width of every box in *boxes*

    :arg width:
      A :class:`float` or an :class:`~symmath.expr.Expr` object.
    :arg boxes:
      An iterable over :class:`~boxes.box.Box` objects.

  """
  for box in boxes:
    box.context.equate(box.width, width)


@public
def height(height, *boxes):
  """

    Constrain the height of every box in *boxes*

    :arg height:
      A :class:`float` or an :class:`~symmath.expr.Expr` object.
    :arg boxes:
      An iterable over :class:`~boxes.box.Box` objects.
  """
  for box in boxes:
    box.context.equate(box.height, height)


@public
def size(size, *boxes):
  """

    Constrain the size of every box in *boxes*

    :arg size:
      A :class:`float` or an :class:`~symmath.expr.Expr` object.
    :arg boxes:
      An iterable over :class:`~boxes.box.Box` objects.
  """
  for box in boxes:
    box.context.equate(box.size, size)


def _pairs(xs):
  return zip(xs[:-1], xs[1:])


def _bbox(boxes):
  return Box(
      context=boxes[0].context,
      top=boxes[0].top,
      right=boxes[-1].right,
      bottom=boxes[-1].bottom,
      left=boxes[0].left,
  )
