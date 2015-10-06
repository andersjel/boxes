from boxes.cartesian import Vect, side_shorthands
from boxes.box import Box, merge_layouts


def align(sides, *boxes):
  layout = merge_layouts(boxes)
  a = boxes[0]
  for b in boxes[1:]:
    for side_shorthand in sides:
      side = side_shorthands[side_shorthand]
      layout.equate(getattr(a, side), getattr(b, side))


def row(*boxes, spacing=0):
  hcat(*boxes, spacing=spacing)
  align("tb", *boxes)
  return _bbox(boxes)


def column(*boxes, spacing=0):
  vcat(*boxes, spacing=spacing)
  align("lr", *boxes)
  return _bbox(boxes)


def hcat(*boxes, spacing=0):
  layout = merge_layouts(boxes)
  for a, b in _pairs(boxes):
    layout.equate(a.right + spacing, b.left)


def vcat(*boxes, spacing=0):
  layout = merge_layouts(boxes)
  for a, b in _pairs(boxes):
    layout.equate(a.bottom + spacing, b.top)


def aspect(aspect, *boxes):
  if isinstance(aspect, Box):
    aspect = aspect.aspect
  for box in boxes:
    box.layout.equate(box.width, box.height*aspect)


def width(width, *boxes):
  if isinstance(width, Box):
    width = width.width
  for box in boxes:
    box.layout.equate(box.width, width)


def height(height, *boxes):
  if isinstance(height, Box):
    height = height.height
  for box in boxes:
    box.layout.equate(box.height, height)


def size(size, *boxes):
  if isinstance(size, Box):
    size = size.size
  for box in boxes:
    box.layout.equate(box.size, size)


def _pairs(xs):
  return zip(xs[:-1], xs[1:])


def _bbox(boxes):
  layout = merge_layouts(boxes)
  return Box(
      layout=layout,
      rect=(boxes[0].top, boxes[-1].right, boxes[-1].bottom, boxes[0].left),
  )
