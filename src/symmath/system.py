from symmath.expr import Expr
from collections import abc


class System:

  def __init__(self):
    self.facts = {}

  def rewrite(self, expr):
    for symbol in list(expr.terms):
      try:
        fact = self.facts[symbol]
      except KeyError:
        continue
      expr.substitue(symbol, fact)

  def simplify(self, expr):
    expr = Expr(expr)
    self.rewrite(expr)
    return expr

  def eval(self, val):
    if hasattr(val, '_symmath_eval'):
      return val._symmath_eval(self.eval)
    return self.simplify(val).scalar()

  def equate(self, a, b):
    if hasattr(a, '_symmath_equate'):
      a._symmath_equate(self.equate, b)
      return
    if hasattr(b, '_symmath_equate'):
      b._symmath_equate(self.equate, a)
      return
    if isinstance(a, abc.Iterable) and isinstance(b, abc.Iterable):
      for x, y in zip(a, b):
        self.equate(x, y)
      return
    expr = self.simplify(a - b)
    if expr == 0:
      return
    # We now have an equation
    #
    #   0 = c_1 x_1 + c_2 x_2 + ...
    #
    # where {x_1, x_2, ... } are symbols. We find the pair (x_i, c_i) where c_i
    # is maximal, as this will lead to the smallest round-off errors later.
    symbol, coef = max(
        ((k, v) for k, v in expr.terms.items() if k is not None),
        key=lambda x: x[1]
    )
    # We now rearrange x_i = (c_1 x_1 + c_2 x_2 + ...) / c_i
    expr[symbol] = 0
    expr /= - coef
    # and substitue this into all the old facts to eliminate x_i.
    for subs in self.facts.values():
      subs.substitue(symbol, expr)
    # finally add x_i as a fact
    self.facts[symbol] = expr
