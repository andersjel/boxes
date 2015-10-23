import symmath.numtype


class System:

  def __init__(self, tolerance=1e-8):
    self.facts = {}
    self.tolerance = tolerance

  def sym(self, key):
    expr = self.zero()
    expr[key] = 1
    return expr

  def zero(self):
    expr = Expr.__new__(Expr)
    expr.system = self
    expr.terms = {}
    return expr


class Expr(symmath.numtype.NumType):

  def __init__(self, other):
    self.system = other.system
    self.terms = other.terms.copy()

  def _to_expr(self, arg):
    if isinstance(arg, Expr):
      assert self.system is arg.system
      return Expr(arg)
    else:
      expr = self.system.zero()
      expr[None] = arg
      return expr

  def __getitem__(self, symbol):
    try:
      return self.terms[symbol]
    except KeyError:
      return 0

  def __setitem__(self, symbol, value):
    if abs(value) < self.system.tolerance:
      self.terms.pop(symbol, None)
    else:
      self.terms[symbol] = value

  def substitue(self, symbol, arg):
    coef = self.terms.pop(symbol, 0)
    self += coef * arg

  def simplify(self):
    for symbol in list(self.terms):
      try:
        expr = self.system.facts[symbol]
      except KeyError:
        continue
      self.substitue(symbol, expr)

  def equate(self, other):
    expr = self - other
    expr.simplify()
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
    for subs in self.system.facts.values():
      subs.substitue(symbol, expr)
    # finally add x_i as a fact
    self.system.facts[symbol] = expr

  def value(self):
    expr = Expr(self)
    expr.simplify()
    value = expr[None]
    assert expr == value
    return value

  def __iadd__(self, other):
    other = self._to_expr(other)
    for s, x in other.terms.items():
      self[s] += x
    return self

  def __imul__(self, val):
    items = self.terms.items()
    self.terms = {}
    for s, x in items:
      self[s] = x * val
    return self

  def __eq__(self, other):
    diff = self - self._to_expr(other)
    return len(diff.terms) == 0

  def __str__(self):
    if len(self.terms) == 0:
      return "0"

    acc = ""

    first = True
    for symbol, val in self.terms.items():
      if val == 0:
        continue

      # Print sign
      if first:
        if val <= 0:
          acc += "-"
      else:
        if val <= 0:
          acc += " − "
        else:
          acc += " + "
      first = False

      has_symbol = symbol is not None

      # Print number and multiplication sign
      if abs(val) != 1 or not has_symbol:
        acc += str(abs(val))
        if has_symbol:
          acc += " "

      # Print symbol
      if has_symbol:
        acc += str(symbol)

    return acc

  def __repr__(self):
    return "{" + str(self) + "}"
