import itertools
from boxes.cartesian import Rect


class Region:

  def __init__(self, layout, rect):
    self.layout = layout
    self.rect = rect

  def pad(self, *args):
    if len(args) > 4:
      raise TypeError(
          'Region.pad(..) takes at most 4 arguments ({} was given).'
          .format(len(args))
      )
    offsets = itertools.islice(itertools.cycle(args), 4)
    rect = Rect._make(
        x + s * y
        for x, s, y in
        zip(self.rect, (1, -1, -1, 1), offsets)
    )
    return Region(self.layout, rect)

  def surround(self, *args):
    return self.pad(*(-x for x in args))

  def fix(self, other):
    layout = merge_layouts((self, other))
    layout.equate(self.rect, other.rect)

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
