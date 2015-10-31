"""
boxes.display
-------------
"""


def display(filename, figure, boxes, dots_per_unit=30):
  import cairo

  is_svg = filename.lower().endswith(".svg")
  figure.solve()

  width, height = (int(x * dots_per_unit) for x in figure.size)
  if is_svg:
    surf = cairo.SVGSurface(filename, width, height)
  else:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  ctx = cairo.Context(surf)
  ctx.scale(dots_per_unit, dots_per_unit)

  ctx.set_source_rgb(0.7, 0.8, 1.0)
  ctx.paint()

  ctx.set_source_rgb(41 / 255, 128 / 255, 185 / 255)
  for box in boxes:
    x, y = box.loc
    w, h = box.size
    ctx.rectangle(x, y, w, h)
  ctx.fill()

  if not is_svg:
    surf.write_to_png(filename)
