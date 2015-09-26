from boxes.symmath import sym
from boxes.cartesian import Rect
from boxes.layout import Layout
from boxes.region import Region


class Box(Region):

  def __init__(self, layout=None):
    Region.__init__(
        self,
        Layout() if layout is None else layout,
        Rect(sym(), sym(), sym(), sym()),
    )
    self.layout.boxes.append(self)
