from boxes import constrain
from boxes.cartesian import Vect, Rect
from boxes.layout import Layout
from boxes.symmath import sym, substitute
import itertools


class Box:

  def __init__(self, layout=None, aspect=None, width=None, height=None):
    self.layout = layout if layout else Layout()
    self._rect = Rect(sym(), sym(), sym(), sym())

    if aspect is not None:
      constrain.aspect(self, aspect)
    if width is not None:
      constrain.width(self, width)
    if height is not None:
      constrain.height(self, height)

  @property
  def rect(self):
    return substitute(self.layout.solution, self._rect, partial=True)

  def fix(self, other):
    layout = merge_layouts((self, other))
    layout.equate(self.rect, other.rect)

  def solve(self, fix_upper_left=True):
    if fix_upper_left:
      self.layout.equate(self.loc, Vect(0, 0))
    return self.layout.solve()

  def pad(self, *args):
    if len(args) > 4:
      raise TypeError(
          'Box.pad(..) takes at most 4 arguments ({} was given).'
          .format(len(args))
      )
    offsets = itertools.islice(itertools.cycle(args), 4)
    rect = Rect._make(
        x + s * y
        for x, s, y in
        zip(self.rect, (1, -1, -1, 1), offsets)
    )
    return Box(self.layout, rect)

  def surround(self, *args):
    return self.pad(*(-x for x in args))

  def __getattr__(self, attr):
    if attr in 'width height top right bottom left loc size'.split():
      return getattr(self.rect, attr)
    raise AttributeError("{} object has no attribute {}.".format(
        repr(self.__class__.__name__), repr(attr)
    ))


def merge_layouts(rs):
  r0 = rs[0]
  for r in rs[1:]:
    r0.layout.merge(r.layout)
  return r0.layout
