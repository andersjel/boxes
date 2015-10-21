class NumType:

  def __add__(self, x):
    y = self.copy()
    y += x
    return y

  def __radd__(self, x):
    return self + x

  def __mul__(self, x):
    y = self.copy()
    y *= x
    return y

  def __rmul__(self, x):
    return self * x

  def __itruediv__(self, x):
    self *= 1 / x
    return self

  def __truediv__(self, x):
    return self * (1 / x)

  def __rtruediv__(self, x):
    return self / x

  def __neg__(self):
    return self * (-1)

  def __isub__(self, other):
    self += -other
    return self

  def __sub__(self, other):
    return self + (-other)

  def __rsub__(self, other):
    return (-self) + other
