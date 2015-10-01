from boxes.box import Box
from boxes.region import Region
from boxes.symmath import sym
from boxes.cartesian import Rect


class Grid(Box):

  def __init__(self, rows, cols, **kwargs):
    Box.__init__(self, **kwargs)
    self.dims_ = [0, 0]
    self.breadths_ = [[], []]
    self.betweens_ = [[sym()], [sym()]]
    self.spacings_ = [[0], [0]]
    for _ in range(rows):
      self.append_row()
    for _ in range(cols):
      self.append_col()
    self.layout.deferred.append(self.deferred_)

  def append_row(self):
    self.breadths_[0].append(sym())
    self.betweens_[0].append(sym())
    self.spacings_[0].append(0)
    self.dims_[0] += 1

  def append_col(self):
    self.breadths_[1].append(sym())
    self.betweens_[1].append(sym())
    self.spacings_[1].append(0)
    self.dims_[1] += 1

  def offset_(self, d, i, include_last_spacing):
    breadths = sum(self.breadths_[d][:i])
    j = i + 1 if include_last_spacing else i
    spacings = sum(self.betweens_[d][:j])
    return breadths + spacings

  def __getitem__(self, idx):
    return GridSlice(self, idx)

  def hspacing(self, i, length):
    self.spacings_[1][i] = length

  def vspacing(self, i, length):
    self.spacings_[0][i] = length

  def update(self, sls):
    super().update(sls)
    self.breadths_ = sls.eval(self.breadths_)
    self.betweens_ = sls.eval(self.betweens_)

  def deferred_(self):
    for i in range(2):
      size = self.offset_(i, self.dims_[i], True)
      self.layout.equate(size, self.size[0 if i == 1 else 1])
      for x, y in zip(self.betweens_[i], self.spacings_[i]):
        self.layout.equate(x, y)


class GridSlice(Region):

  def __init__(self, grid, idx):
    self.grid = grid
    self.spec = _slice_or_index_to_spec(grid.dims_, idx)
    ((r0, r1), (c0, c1)) = self.spec
    rect = Rect(
        grid.top + grid.offset_(0, r0, True),
        grid.left + grid.offset_(1, c1, False),
        grid.top + grid.offset_(0, r1, False),
        grid.left + grid.offset_(1, c0, True),
    )
    Region.__init__(self, grid.layout, rect)

  def spacing(self, l):
    self.hspacing(l)
    self.vspacing(l)

  def vspacing(self, l):
    for i in range(self.spec[0][0] + 1, self.spec[0][1]):
      self.grid.spacings_[0][i] = l

  def hspacing(self, l):
    for i in range(self.spec[1][0] + 1, self.spec[1][1]):
      self.grid.spacings_[1][i] = l


def _slice_or_index_to_spec(dims, idx):
  if not len(idx) == 2:
    raise ValueError
  rval = []
  for i, dim in zip(idx, dims):
    if isinstance(i, slice):
      indices = i.indices(dim)
      if indices[2] != 1:
        raise ValueError
      rval.append(tuple(indices[:2]))
    else:
      if i < 0:
        i = dim + i
      if not 0 <= i < dim:
        raise ValueError
      rval.append((i, i + 1))
  return tuple(rval)
