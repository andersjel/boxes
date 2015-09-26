from boxes.symmath import sym
from boxes.cartesian import Vect
from boxes.layout import Layout
from boxes.region import Region


class Box(Region):

  def __init__(self, layout=None):
    Region.__init__(
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
