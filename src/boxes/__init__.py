from boxes.symmath import sym, Expr, solve_harder
from itertools import chain
from collections.abc import Iterable

class Box:
    def __init__(self, width=None, height=None, aspect=None):
        size = (width, height)
        size = tuple(sym() if x is None else x for x in size)
        self.size = size
        self.loc = (sym(), sym())
        self._eqs = []
        self.children = []
        if aspect is not None:
            self.eq(self.size[0] - self.size[1]*aspect)

    def eq(self, e):
        self._eqs.append(e)

    def eqs(self):
        return chain(self._eqs, *(c.eqs() for c in self.children))

    def solve(self, eqs=()):
        return solve_harder(chain(eqs, self.eqs()))

    def walk(self):
        """Iterate over this box, all children and all grand children"""
        done = set()
        remaining = [self]
        while remaining:
            box = remaining.pop()
            if box in done:
                continue
            done.add(box)
            yield box
            remaining.extend(box.children)

def _slice_or_index_to_spec(dims, idx):
    if not len(idx) == 2: raise ValueError
    def spec():
        for i, dim in zip(reversed(idx), dims):
            if isinstance(i, slice):
                indices = i.indices(dim)
                if indices[2] != 1: raise ValueError
                yield tuple(indices[:2])
            else:
                i %= dim
                if not 0 <= i < dim: raise ValueError
                yield (i, i + 1)
    return tuple(spec())

class Grid(Box):
    def __init__(self, rows, cols, **kwargs):
        margins = {}
        for m in ['all', 'top', 'right', 'bottom', 'left']:
            margins[m] = kwargs.pop(m, None)
        Box.__init__(self, **kwargs)
        self.dims = (cols, rows)
        def syms(n):
            return [sym() for _ in range(n)]
        def tuple_of_syms(ns):
            return tuple(syms(n) for n in ns)
        self.breadths = tuple_of_syms(self.dims)
        self.betweens = tuple_of_syms(n + 1 for n in self.dims)
        self.spacings = tuple([0]*(n + 1) for n in self.dims)
        self.margins(**margins)

    @classmethod
    def mk(clss, content, **kwargs):
        if isinstance(content, Iterable):
            content = list(content)
        else:
            content = [content]
        if isinstance(content[0], Iterable):
            content = [list(x) for x in content]
        else:
            content = [content]
        rows = len(content)
        cols = len(content[0])
        gr = clss(rows, cols, **kwargs)
        for i in range(rows):
            for j in range(cols):
                e = content[i][j]
                if not e: continue
                gr[i, j].fix(e)
        return gr

    def offset(self, d, i, include_last_spacing):
        breadths = sum(self.breadths[d][:i])
        j = i + 1 if include_last_spacing else i
        spacings = sum(self.betweens[d][:j])
        return breadths + spacings

    def __getitem__(self, idx):
        return GridSlice(self, idx)

    def hspacing(self, i, l):
        self.spacings[0][i] = l
    def vspacing(self, i, l):
        self.spacings[1][i] = l

    def margins(self, all=None, top=None, right=None, bottom=None, left=None):
        if all is not None:
            self.margins(top=all, right=all, bottom=all, left=all)
        if top    is not None: self.vspacing(0,  top)
        if right  is not None: self.hspacing(-1, right)
        if bottom is not None: self.vspacing(-1, bottom)
        if left   is not None: self.hspacing(0,  left)

    def eqs(self):
        for d in range(2):
            size = self.offset(d, self.dims[d] + 1, True)
            yield size - self.size[d]
            for x, y in zip(self.betweens[d], self.spacings[d]):
                yield y - x
        yield from super().eqs()

class GridSlice:
    def __init__(self, grid, idx):
        self.grid = grid
        self.spec = _slice_or_index_to_spec(grid.dims, idx)

    def fix(self, child, **kwargs):
        if kwargs or isinstance(child, Iterable):
            box = Grid.mk(child, **kwargs)
            self.fix(box)
            return
        gr = self.grid
        for d, s in enumerate(self.spec):
            s0, s1 = s
            # fix the size of the child
            size = gr.offset(d, s1, False) - gr.offset(d, s0, True)
            self.grid.eq(size - child.size[d])
            # fix the location of the child
            loc = gr.loc[d] + gr.offset(d, s0, True)
            self.grid.eq(loc - child.loc[d])
        self.grid.children.append(child)

    def spacing(self, l):
        self.hspacing(l)
        self.vspacing(l)
    def hspacing(self, l):
        for i in range(self.spec[0][0] + 1, self.spec[0][1]):
            self.grid.spacings[0][i] = l
    def vspacing(self, l):
        for i in range(self.spec[1][0] + 1, self.spec[1][1]):
            self.grid.spacings[1][i] = l

class Figure:
    def __init__(self, size):
        self.size = size

    def place(self, box, loc, size):
        x, y = loc
        w, h = size
        w_, h_ = self.size
        box.locf = (x/w_, (h_-y-h)/h_)
        box.sizef = (w/w_, h/h_)
        box.rectf = tuple(chain(box.locf, box.sizef))

    def conv_size(self, unit=2.54):
        return tuple(x/unit for x in self.size)

def place_all(layout, eqs=(), figure_class=Figure):
    """Solve a layout, create a figure the same size, and place every box in the figure.

    Args:
        layout:
            The content of the figure.
        eqs:
            Extra equations to use when solving the layout.
        figure_class:
            The class of the figure to make.
    Returns:
        A tuple (figure, sls) where figure is an instance figure_class and sls
        is the result of calling layout.solve.
    Side effects:
        Calls figure.place(box, loc, size) for all boxes in the figure.
    """
    eqs = chain(eqs, layout.loc)  # put the layout at (0, 0)
    sls = layout.solve(eqs)
    figure = figure_class(sls.eval(layout.size))
    for box in layout.walk():
        figure.place(box, sls.eval(box.loc), sls.eval(box.size))
    return figure, sls
