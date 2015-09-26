from boxes.box import Box


class Grid(Box):

  def __init__(self, rows, cols, **kwargs):
    Box.__init__(self, **kwargs)
    self.dims_ = [0, 0]
    self.breadths_ = [[], []]
    self.betweens_ = [[sym()], [sym()]]
    self.spacings_ = [0, 0]
    for _ in range(rows):
      self.append_row()
    for _ in range(cols):
      self.append_col()

  def append_row(self):
    self.breadths_[0].append(sym())
    self.betweens_[0].append(sym())
    self.spacings_[0].append(0)
    self.dims_[0] += 1

  def append_col(self):
    self.breadths_[1].append(sym())
    self.betweens_[1].append(sym())
    self.spacings_[1].append(0)
    self.dims_[0] += 1

  def offset_(self, d, i, include_last_spacing):
    breadths = sum(self.breadths_[d][:i])
    j = i + 1 if include_last_spacing else i
    spacings = sum(self.betweens_[d][:j])
    return breadths + spacings

  def __getitem__(self, idx):
    return GridSlice(self, idx)

  def hspacing(self, i, length):
    self.spacings_[0][i] = length

  def vspacing(self, i, length):
    self.spacings_[1][i] = length


class GridSlice(Region):

  def __init__(self, grid, idx):
    self.grid = grid
    self.spec = _slice_or_index_to_spec(grid.dims, idx)
    ((r0, r1), (c0, c1)) = self.spec
    rect = Rect(
        gr.offset_(0, r0, True),
        gr.offset_(1, c1, False),
        gr.offset_(0, r1, False),
        gr.offset_(1, c0, True),
    )
    Region.__init__(self, grid.layout, rect)
    self.layout.deferred.append(self.deferred_)

  def spacing(self, l):
    self.hspacing(l)
    self.vspacing(l)

  def hspacing(self, l):
    for i in range(self.spec[0][0] + 1, self.spec[0][1]):
      self.grid.spacings_[0][i] = l

  def vspacing(self, l):
    for i in range(self.spec[1][0] + 1, self.spec[1][1]):
      self.grid.spacings_[1][i] = l

  def deferred_(self):
    for i in range(2):
      size = self.offset(i, self.dims[i] + 1, True)
      self.layout.equate(size, self.size[i])
      for x, y in zip(self.betweens[i], self.spacings[i]):
        self.layout.equate(x, y)


def _slice_or_index_to_spec(dims, idx):
  if not len(idx) == 2:
    raise ValueError
  rval = []
  for i, dim in zip(reversed(idx), dims):
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
