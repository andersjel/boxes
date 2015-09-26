import itertools
from boxes.cartesian import Vect, Rect


class Region:

  def __init__(self, layout, loc, size):
    self.layout = layout
    self.loc = Vect(loc)
    self.size = Vect(size)

    self.width = size.x
    self.height = size.y
    self.rect = Rect(
        loc.y,
        loc.x + size.x,
        loc.y + size.y,
        loc.x,
    )
    self.__dict__.update(self.rect._as_dict())

  def pad(self, *args):
    if len(args) > 4:
      raise TypeError(
          'Region.pad(..) takes at most 4 arguments ({} was given).'
          .format(len(args))
      )
      offsets = itertools.islice(itertools.cycle(args), 4)
      offsets = (s * offsets[i] for i, s in enumerate((1, -1, -1, 1)))
      rect = Rect(x + y for x, y in zip(self.rect, offsets))

      return region_from_rect(self.layout, rect)

  def margins(self, *args):
    return self.pad(*(-x for x in args))

  def fix(self, other):
    self.layout.merge(other.layout)
    for x, y in zip(self.rect, other.rect):
      self.layout.equate(x, y)

def region_from_rect(layout, rect):
  rect = Rect(rect)
  loc = Vect(rect.left, rect.top)
  size = Vect(rect.width, rect.height)
  return Region(layout, loc, size)
