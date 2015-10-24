from symmath import *


def near(x, y):
  return abs(x - y) < 1e-7


def test_solve():
  sys = System()
  x, y, z = (sym(n) for n in "xyz")
  sys.equate(x + y, z)
  sys.equate(x - y, 2 * z)
  sys.equate(x + y + z, 4)
  assert near(sys.eval(x), 3)
  assert near(sys.eval(y), -1)
  assert near(sys.eval(z), 2)
