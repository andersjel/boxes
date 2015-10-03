from boxes.cartesian import Vect, side_shorthands
from boxes.region import Region, merge_layouts


def align(sides, *rs):
  layout = merge_layouts(rs)
  a = rs[0]
  for b in rs[1:]:
    for side_shorthand in sides:
      side = side_shorthands[side_shorthand]
      layout.equate(getattr(a, side), getattr(b, side))


def row(*rs, spacing=0):
  hcat(*rs, spacing=spacing)
  align("tb", *rs)
  return _bbox(rs)


def column(*rs, spacing=0):
  vcat(*rs, spacing=spacing)
  align("lr", *rs)
  return _bbox(rs)


def hcat(*rs, spacing=0):
  layout = merge_layouts(rs)
  for a, b in _pairs(rs):
    layout.equate(a.right + spacing, b.left)


def vcat(*rs, spacing=0):
  layout = merge_layouts(rs)
  for a, b in _pairs(rs):
    layout.equate(a.bottom + spacing, b.top)


def aspect(rect, aspect):
  rect.layout.equate(rect.width, rect.height*aspect)


def width(rect, width):
  rect.layout.equate(rect.width, width)


def height(rect, height):
  rect.layout.equate(rect.height, height)


def _pairs(xs):
  return zip(xs[:-1], xs[1:])


def _bbox(rs):
  layout = merge_layouts(rs)
  return Region(
      layout, (rs[0].top, rs[-1].right, rs[-1].bottom, rs[0].left)
  )
