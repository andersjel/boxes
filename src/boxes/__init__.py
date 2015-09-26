from boxes.box import Box
from boxes.grid import Grid
from boxes.constrain import *


# TODO Remove everthing below

def _slice_or_index_to_spec(dims, idx):
  if not len(idx) == 2:
    raise ValueError

  def spec():
    for i, dim in zip(reversed(idx), dims):
      if isinstance(i, slice):
        indices = i.indices(dim)
        if indices[2] != 1:
          raise ValueError
        yield tuple(indices[:2])
      else:
        i %= dim
        if not 0 <= i < dim:
          raise ValueError
        yield (i, i + 1)
  return tuple(spec())


class Grid(Box):

  def __init__(self, rows, cols, **kwargs):
    margins = {}
    for m in ['all', 'top', 'right', 'bottom', 'left', 'hor', 'vert']:
      margins[m] = kwargs.pop(m, None)
    Box.__init__(self, **kwargs)
    self.dims = (cols, rows)

    def syms(n):
      return [sym() for _ in range(n)]

    def tuple_of_syms(ns):
      return tuple(syms(n) for n in ns)
    self.breadths = tuple_of_syms(self.dims)
    self.betweens = tuple_of_syms(n + 1 for n in self.dims)
    self.spacings = tuple([0] * (n + 1) for n in self.dims)
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
        if not e:
          continue
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

  def margins(self,
              all=None,
              top=None, right=None, bottom=None, left=None,
              hor=None, vert=None,
              ):
    if all is not None:
      self.margins(top=all, right=all, bottom=all, left=all)
    if hor is not None:
      self.margins(left=hor, right=hor)
    if vert is not None:
      self.margins(top=vert, bottom=vert)
    if top is not None:
      self.vspacing(0,  top)
    if right is not None:
      self.hspacing(-1, right)
    if bottom is not None:
      self.vspacing(-1, bottom)
    if left is not None:
      self.hspacing(0,  left)

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
