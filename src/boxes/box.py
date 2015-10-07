from boxes.cartesian import Vect, Rect
from boxes.layout import Layout
from symmath import sym, substitute
import itertools


class Box:

  _rect_attrs = set('width height top right bottom left loc size'.split())

  def __init__(self, layout=None, aspect=None, rect=None, **kwargs):
    self.layout = layout if layout else Layout()
    self._rect = Rect._make(rect) if rect else Rect(sym(), sym(), sym(), sym())

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
    return Box(layout=self.layout, rect=rect)

  def surround(self, *args):
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


def merge_layouts(bs):
  r0 = bs[0]
  for r in bs[1:]:
    r0.layout.merge(r.layout)
  return r0.layout
