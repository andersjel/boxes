import itertools
from boxes.cartesian import Rect


class Region:

  def __init__(self, layout, rect):
    self.layout = layout
    self.rect = rect

    for prop in 'width height top right bottom left loc size'.split():
      setattr(self, prop, getattr(rect, prop))

  def pad(self, *args):
    if len(args) > 4:
      raise TypeError(
          'Region.pad(..) takes at most 4 arguments ({} was given).'
          .format(len(args))
      )
      offsets = itertools.islice(itertools.cycle(args), 4)
      rect = Rect(
          x + s * y
          for x, s, y in
          zip(self.rect, (1, -1, -1, 1), offsets)
      )
      return Region(self.layout, rect)

  def surround(self, *args):
    return self.pad(*(-x for x in args))

  def fix(self, other):
    layout = merge_layouts((self, other))
    layout.equate(x.rect, y.rect)


def merge_layouts(rs):
  r0 = rs[0]
  for r in rs[1:]:
  r0.layout.merge(r.layout)
  return r0.layout
