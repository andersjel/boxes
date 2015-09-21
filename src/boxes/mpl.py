import boxes
from boxes import Grid, Box
from matplotlib import pyplot

text_height = 0.47
text_drop = 0.1


class Plot(Box):

  def draw(self, **kwargs):
    rectf = self.locf + self.sizef
    return self.fig.add_axes(rectf, **kwargs)


class Text(Grid):

  def __init__(
      self,
      text=None,
      vertical=False,
      align='c',
      valign='b',
      color='black',
      text_height=text_height,
      text_options=None,
      expand=False,
      **kwargs
  ):
    self.text_box = Box()
    if expand:
      Grid.__init__(
          self, 1, 1,
          **kwargs
      )
    elif vertical:
      Grid.__init__(
          self, 1, 1,
          width=text_height,
          **kwargs
      )
    else:
      Grid.__init__(
          self, 1, 1,
          height=text_height,
          bottom=text_drop,
          **kwargs
      )
    self[0, 0].fix(self.text_box)
    self.vertical = vertical
    self.align = align
    self.valign = valign
    self.text = text
    self.color = color
    self.text_options = text_options

  def auto(self):
    if self.text is not None:
      self.draw(self.text)

  def draw(self, text=None, **kwargs):
    if text is None:
      text = self.text
    x, y = self.text_box.locf
    w, h = self.text_box.sizef
    kws = {
        'ha': 'center',
        'va': 'baseline',
        'color': self.color,
    }
    ly = y
    if (not self.vertical) and self.align == 'c':
      lx = x + w / 2
    elif (not self.vertical) and self.align == 'r':
      kws['ha'] = 'right'
      lx = x + w
    elif (not self.vertical) and self.align == 'l':
      kws['ha'] = 'left'
      lx = x
    elif self.vertical and self.align == 'c':
      kws['va'] = 'center'
      kws['rotation'] = 'vertical'
      lx = x + w / 2
      ly = y + h / 2
    else:
      raise NotImplemented
    if self.valign == 'c':
      ly = y + h / 2
    kws.update(kwargs)
    if self.text_options is not None:
      kws.update(self.text_options)
    return self.fig.text(lx, ly, text, **kws)


class Colorbar(Grid):

  def __init__(self, text_width=0.6):
    self.box = Plot(width=0.2)
    Grid.__init__(self, 1, 1, right=text_width)
    self[0, 0].fix(self.box)

  def draw(self, im, **kwargs):
    cax = self.box.draw()
    cbar = self.fig.colorbar(im, cax=cax, **kwargs)
    cbar.solids.set_edgecolor("face")
    cax.tick_params(axis='y', right=False)
    ticks = cax.yaxis.get_major_ticks()
    if len(ticks) == 2:
      ticks[0].label2.set_verticalalignment('bottom')
      ticks[-1].label2.set_verticalalignment('top')
    return cbar


def glue(layout, units_per_inch=2.54, solution=None):
  """Use a set of boxes to template a matplotlib figure.

  This function solves `layout`, which should be a Box instance, and adds the
  following attributes to every box in `layout`:
  - fig: a newly created matplotlib Figure sized to match the layout.
  - locf: the location of the box relative to the size of the figure using
      matplotlib's coordinate system.
  - sizef: the size of the box relative to the size of the layout.

  After the attributes have been added. box.auto() is called for every box in
  the layout if it has this function.

  Keyword arguments:
  - units_per_inch:
      This is used to convert the units used by the layout to inches. The
      default of 2.54 assumes you are using cm's as the unit for the layout.
  - solution:
      Pass in a solution for the layout obtained by calling layout.solve(). If
      this is None, glue() will call layout.solve() for you.
  Returns: A newly created matplotlib figure.
  """
  if not solution:
    solution = layout.solve()
  size = solution.eval(layout.size)
  size_in_inches = tuple(v / units_per_inch for v in size)
  figure = pyplot.figure(figsize=size_in_inches)
  W, H = size
  # We monkey-patch every box with its final position using the coordinate
  # system matplotlib expects for laying out axes (which is relative to the
  # figure size).
  for box in layout.walk():
    x, y = solution.eval(box.loc)
    w, h = solution.eval(box.size)
    box.fig = figure
    box.locf = (x / W, (H - y - h) / H)
    box.sizef = (w / W, h / H)
  for box in layout.walk():
    if hasattr(box, 'auto'):
      box.auto()
  return figure
