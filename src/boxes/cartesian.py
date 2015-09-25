from collections import namedtuple


class vect(namedtuple('vect', 'x y')):

  def __add__(self, other):
    return vect(u + v for u, v in zip(self, other))

  def __sub__(self, other):
    return vect(u - v for u, v in zip(self, other))


side_shorthands = {
    't': 'top',
    'b': 'bottom',
    'l': 'left',
    'r': 'right',
}
