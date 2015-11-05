"""
boxes.box
---------

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

  .. attribute:: context

    The :class:`boxes.context.Context` of this box.

"""

from boxes.cartesian import Vect, Rect
import itertools


class Box:
  """

    Represents a rectangle in the latout. The position of the rectangle is given
    by the :attr:`rect` property.

    All keyword arguments to the constructor are optional, and the same effect
    can be obtained by later constraining the box.

    :arg boxes.context.Context context:
      The context the box belongs to.
    :arg boxes.cartesian.Rect rect:
      Explicitly locate the box.
    :arg float aspect:
      Forwarded to :func:`boxes.constrain.aspect`.

    In addition, any property of :class:`~boxes.cartesian.Rect` can be used as a
    keyword argument to the constructor, which will introduce a constraint.

    Note, that :class:`Box` instances can also be obtained by calling the
    :meth:`~boxes.context.Context.box` method of a
    :class:`~boxes.context.Context` instance.

  """

  _rect_attrs = set('width height top right bottom left loc size'.split())

  def __init__(self, context, rect=None, aspect=None, **kwargs):
    self.context = context
    if rect is None:
      rect = Rect(*(context.sym() for _ in range(4)))
    self._rect = rect

    for k, v in kwargs.items():
      if k in self._rect_attrs:
        if v is not None:
          self.context.equate(getattr(self.rect, k), v)
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
      until you :func:`solve` the context.

    """
    if self.context.is_solved:
      return self.context.system.eval(self._rect)
    return self._rect

  def solve(self, fix_upper_left=True):
    """

    Calling this method has two effects:

    #.  If *fix_upper_left* is True (the default), a constraint is added
        setting ``self.loc == (0, 0)``.
    #.  :func:`~boxes.context.Context.solve` is called on :attr:`Box.context`.

    >>> from boxes import Context
    >>> ctx = Context()
    >>> box = ctx.box(size=(6.0, 10.0))
    >>> (box.width, box.height)
    (Expr(x1 - x3), Expr(-x0 + x2))
    >>> box.solve()
    >>> (box.width, box.height)
    (6.0, 10.0)

    """
    if fix_upper_left:
      self.context.equate(self.loc, Vect(0, 0))
    return self.context.solve()

  def fix(self, other):
    """Constrain this box and *other* to have the same size and position."""
    self.context.equate(self.rect, other.rect)

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

      >>> from boxes import *
      >>> ctx = Context()
      >>> outer_box = ctx.box(width=10)
      >>> inner_box = ctx.box(height=4)
      >>> outer_box.pad(0.5).fix(inner_box)
      >>> outer_box.solve()
      >>> print(outer_box.loc, outer_box.size)
      (0.0, 0.0) (10.0, 5.0)
      >>> print(inner_box.loc, inner_box.size)
      (0.5, 0.5) (9.0, 4.0)

      .. rubric:: Center a box inside another

      >>> from boxes import *
      >>> ctx = Context()
      >>> outer_box = ctx.box(size=(6, 5))
      >>> inner_box = ctx.box(size=(4, 4))
      >>> outer_box.pad(ctx.sym(), ctx.sym()).fix(inner_box)
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
    return Box(self.context, rect=rect)

  def surround(self, *args):
    """

      Similar to :func:`pad`, but the arguments are negated.

    """
    return self.pad(*(-x for x in args))

  def __getattr__(self, attr):
    if attr in self._rect_attrs:
      return getattr(self.rect, attr)
    raise AttributeError
