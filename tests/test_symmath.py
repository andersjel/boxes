from symmath import *

def near(x, y):
  return abs(x - y) < 1e-7

def test_solve():
  system = System()
  x, y, z = [system.sym(n) for n in "xyz"]
  (x + y).equate(z)
  (x - y).equate(2 * z)
  (x + y + z).equate(4)
  assert near(x.value(), 3)
  assert near(y.value(), -1)
  assert near(z.value(), 2)
