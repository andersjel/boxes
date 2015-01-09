import boxes
from boxes import Grid, Box
from matplotlib import pyplot

text_height  = 0.47
text_drop    = 0.1

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
            color='black',
            text_height=text_height,
            **kwargs
        ):
        self.text_box = Box()
        if vertical:
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
        self.text = text
        self.color = color

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
        kws.update(kwargs)
        if (not self.vertical) and self.align == 'c':
            l = (x + w/2, y)
        elif (not self.vertical) and self.align == 'r':
            kws['ha'] = 'right'
            l = (x + w, y)
        elif (not self.vertical) and self.align == 'l':
            kws['ha'] = 'left'
            l = (x, y)
        elif self.vertical and self.align == 'c':
            kws['va'] = 'center'
            kws['rotation'] = 'vertical'
            l = (x + w/2, y + h/2)
        else:
            raise NotImplemented
        return self.fig.text(l[0], l[1], text, **kws)

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
    size_in_inches = tuple(v/units_per_inch for v in size)
    figure = pyplot.figure(figsize=size_in_inches)
    W, H = size
    # We monkey-patch every box with its final position using the coordinate
    # system matplotlib expects for laying out axes (which is relative to the
    # figure size).
    for box in layout.walk():
        x, y = solution.eval(box.loc)
        w, h = solution.eval(box.size)
        box.fig = figure
        box.locf = (x/W, (H - y - h)/H)
        box.sizef = (w/W, h/H)
    for box in layout.walk():
        if hasattr(box, 'auto'):
            box.auto()
    return figure
