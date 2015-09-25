from boxes.symmath import sym
from boxes.cartesian import vect
from boxes.layout import Layout


class Rect:

  def __init__(self, layout, loc, size):
    self.layout = layout
    self.loc = loc
    self.size = size

    # TODO Make these properties
    self.left = loc.x
    self.right = loc.x + size.x
    self.top = loc.y
    self.bottom = loc.y + size.y
    self.width = size.x
    self.height = size.y


class Box(Rect):

  def __init__(self, layout=None):
    Rect.__init__(
        self,
        Layout() if layout is None else layout,
        vect(sym(), sym()),
        vect(sym(), sym()),
    )
    self.layout.boxes.append(self)


def merge_layouts(rs):
  r0 = rs[0]
  for r in rs[1:]:
    r0.layout.merge(r.layout)
  return r0.layout
