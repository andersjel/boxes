import collections.abc


class MergeList(collections.abc.MutableSequence):

  def __init__(self, vals=[]):
    self.parent_ = None
    self.rank_ = 0
    self.vals_ = vals

  @property
  def root_(self):
    if self.parent_ is None:
      return self
    self.parent_ = self.parent_.root_
    return self.parent_

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
    self.vals_ += other.vals_
    del other.vals_

  @property
  def items_(self):
    return self.root_.vals_

  def __getitem__(self, i):
    return self.items_[i]

  def __setitem__(self, i, v):
    self.items_[i] = v

  def __delitem__(self, i):
    del self.items_[i]

  def __len__(self):
    return len(self.items_)

  def insert(self, *args):
    self.items_.insert(*args)
