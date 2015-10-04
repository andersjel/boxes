from boxes.cartesian import Vect, side_shorthands
from boxes.box import Box, merge_layouts


def align(sides, *bs):
  layout = merge_layouts(bs)
  a = bs[0]
  for b in bs[1:]:
    for side_shorthand in sides:
      side = side_shorthands[side_shorthand]
      layout.equate(getattr(a, side), getattr(b, side))


def row(*bs, spacing=0):
  hcat(*bs, spacing=spacing)
  align("tb", *bs)
  return _bbox(bs)


def column(*bs, spacing=0):
  vcat(*bs, spacing=spacing)
  align("lr", *bs)
  return _bbox(bs)


def hcat(*bs, spacing=0):
  layout = merge_layouts(bs)
  for a, b in _pairs(bs):
    layout.equate(a.right + spacing, b.left)


def vcat(*bs, spacing=0):
  layout = merge_layouts(bs)
  for a, b in _pairs(bs):
    layout.equate(a.bottom + spacing, b.top)


def aspect(box, aspect):
  box.layout.equate(box.width, box.height*aspect)


def width(box, width):
  box.layout.equate(box.width, width)


def height(box, height):
  box.layout.equate(box.height, height)


def size(box, size):
  box.layout.equate(box.size, size)


# TODO
# Change aspect, width, height, size so the call looks like:
# height(height, *bs) or height(*bs).


def _pairs(xs):
  return zip(xs[:-1], xs[1:])


def _bbox(bs):
  layout = merge_layouts(bs)
  return Box(
      layout=layout,
      rect=(bs[0].top, bs[-1].right, bs[-1].bottom, bs[0].left),
  )
