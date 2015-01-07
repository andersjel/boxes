import boxes
from boxes import Grid, Box
from matplotlib import pyplot

text_height  = 0.47
text_drop    = 0.1

class Plot(Box):
    def draw(self, **kwargs):
        return self.fig.add_axes(self.rectf, **kwargs)

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

def layout_to_mpl(layout, *args, **kwargs):
    figure, sls = boxes.place_all(layout, *args, **kwargs)
    size = figure.conv_size()
    mpl_figure = pyplot.figure(figsize=size)

    for box in layout.walk():
        box.fig = mpl_figure
    for box in layout.walk():
        if hasattr(box, 'auto'):
            box.auto()

    return mpl_figure, figure, sls
