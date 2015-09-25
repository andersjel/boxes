from boxes.cartesian import vect, side_shorthands
from boxes.box import merge_layouts


def align(sides, *rs):
  layout = merge_layouts(rs)
  a = rs[0]
  for b in rs[1:]:
    for side_shorthand in sides:
      side = side_shorthands[side_shorthand]
      layout.equate(getattr(a, side), getattr(b, side))


def pairs_(xs):
  return zip(xs[:-1], xs[1:])


def hcat(*rs, spacing=0):
  layout = merge_layouts(rs)
  for a, b in pairs_(rs):
    layout.equate(a.right + spacing, a.left)


def vcat(*rs, spacing=0):
  layout = merge_layouts(rs)
  for a, b in pairs_(rs):
    layout.equate(a.bottom + spacing, a.top)


def bbox_(rs):
  loc = vect(rs[0].left, rs[0].top)
  rloc = vect(rs[-1].right, rs[-1].bottom)
  size = vect(*(rloc - loc))
  return Rect(rs[0].layout, loc, size)


def hjoin(*rs, spacing=0):
  hcat(*rs, spacing=spacing)
  align("tb", *rs)
  return bbox_(rs)


def vjoin(*rs, spacing=0):
  vcat(*rs, spacing=spacing)
  align("lr", *rs)
  return bbox_(rs)
