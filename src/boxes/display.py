import cairo
from boxes import merge_layouts


def display(filename, figure, boxes, dots_per_unit=30):
  figure.layout.merge(merge_layouts(boxes))
  figure.solve()

  width, height = (int(x * dots_per_unit + 0.5) for x in figure.size)
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  ctx = cairo.Context(surf)
  ctx.scale(dots_per_unit, dots_per_unit)

  ctx.set_source_rgb(0.8, 0.8, 0.8)
  ctx.paint()

  ctx.set_source_rgb(0.4, 0.4, 0.4)
  for box in boxes:
    x, y = box.loc
    w, h = box.size
    ctx.rectangle(x, y, w, h)
  ctx.fill()

  surf.write_to_png(filename)
