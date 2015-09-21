class DisjointSet:

  def __init__(self, val):
    self.parent_ = None
    self.rank_ = 0
    self.val_ = val

  @property
  def root_(self):
    if self.parent_ is None:
      return self
    self.parent_ = self.parent_.root_
    return self.parent_

  @property
  def val(self):
    return self.root_.val_

  @val.setter
  def val(self, val):
    self.root_.val_ = val

  def merge(self, other):
    x = self.root_
    y = other.root_
    if x is y:
      return
    if x.rank_ < y.rank_:
      y.absorb_(x)
    elif y.rank_ < x.rank_:
      x.absorb_(y)
    else:
      x.absorb_(y)
      x.rank_ += 1

  def absorb_(self, other):
    assert(self.parent_ is None)
    assert(other.parent_ is None)
    other.parent_ = self
    del other.rank_
    self.val_ += other.val_
    del other.val_
