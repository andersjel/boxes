from boxes.symmath import sym
from boxes.cartesian import Rect
from boxes.layout import Layout
from boxes.region import Region
from boxes import constrain


class Box(Region):

  def __init__(self, region=None, aspect=None, width=None, height=None):
    if region is None:
      rect = Rect(sym(), sym(), sym(), sym())
      Region.__init__(self, Layout(), rect)
    else:
      Region.__init__(self, region.layout, region.rect)
    self.layout.boxes.append(self)

    if aspect is not None:
      constrain.aspect(self, aspect)
    if width is not None:
      constrain.width(self, width)
    if height is not None:
      constrain.height(self, height)
