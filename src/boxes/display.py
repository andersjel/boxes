"""
boxes.display
-------------
"""


def display(filename, figure, boxes, dots_per_unit=30):
  """

  Output a figure showing the location of the given *boxes* to *filename*. This
  function calls ``figure.solve()`` and uses the size of ``figure`` as the size
  of the image. This function is meant for quick visualization.

  :arg string filename: The output file. Must end in ``.svg`` or ``.png``.
  :arg figure: Defines the size of the figure.
  :type figure: :class:`~boxes.box.Box`
  :arg boxes: The boxes to draw.
  :type boxes: An iterable of :class:`~boxes.box.Box` instances
  :arg float dots_per_unit: Scaling factor.

  """
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
