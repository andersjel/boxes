import collections.abc


class Merge:

  def __init__(self, content):
    self.__parent = None
    self.__rank = 0
    self.__content = content

  @property
  def __root(self):
    if self.__parent is None:
      return self
    self.__parent = self.__parent.__root
    return self.__parent

  @property
  def _content(self):
    return self.__root.__content

  def merge(self, other):
    x = self.__root
    y = other.__root
    if x is y:
      return
    if x.__rank < y.__rank:
      y.__absorb(x)
    elif y.__rank < x.__rank:
      x.__absorb(y)
    else:
      x.__absorb(y)
      x.__rank += 1

  def __absorb(self, other):
    assert(self.__parent is None)
    assert(other.__parent is None)
    other.__parent = self
    del other.__rank
    self.__content = self._combine(self.__content, other.__content)
    del other.__content

  @staticmethod
  def _combine(x, y):
    return x + y


class MergeList(Merge, collections.abc.MutableSequence):

  def __init__(self):
    Merge.__init__(self, [])

  def __getitem__(self, i):
    return self._content[i]

  def __setitem__(self, i, v):
    self._content[i] = v

  def __delitem__(self, i):
    del self._content[i]

  def __len__(self):
    return len(self._content)

  def insert(self, *args):
    self._content.insert(*args)

  def clear(self):
    self._content.clear()


class MergeDict(Merge, collections.abc.MutableMapping):

  def __init__(self):
    Merge.__init__(self, {})

  @staticmethod
  def _combine(x, y):
    return dict(x, **y)

  def __getitem__(self, i):
    return self._content[i]

  def __setitem__(self, i, v):
    self._content[i] = v

  def __delitem__(self, i):
    del self._content[i]

  def __len__(self):
    return len(self._content)

  def __iter__(self):
    return self._content.__iter__()

  def clear(self):
    self._content.clear()
