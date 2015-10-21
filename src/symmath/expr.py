import symmath.numtype


class System:

  def __init__(self, tolerance=1e-8):
    self.facts = {}
    self.tolerance = tolerance

  def sym(self, key):
    return Expr(self, {key: 1})


class Expr(symmath.numtype.NumType):

  def __init__(self, system, terms):
    self.system = system
    self.terms = terms

  def copy(self):
    return Expr(self.system, self.terms.copy())

  def _to_expr(self, arg):
    if isinstance(arg, Expr):
      assert arg.system is self.system
      return arg
    expr = Expr(self.system, {})
    expr._set(None, arg)
    return expr

  def _set(self, symbol, value):
    if abs(value) < self.system.tolerance:
      try:
        del self.terms[symbol]
      except KeyError:
        pass
    else:
      self.terms[symbol] = value

  def substitue(self, symbol, arg):
    expr = self._to_expr(arg)
    try:
      coef = self.terms.pop(symbol)
    except KeyError:
      return
    self += coef * expr

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
    symbol, coef = max(
        ((k, v) for k, v in expr.terms.items() if k is not None),
        key=lambda x: x[1]
    )
    expr.substitue(symbol, 0)
    expr /= - coef
    for subs in self.system.facts.values():
      subs.substitue(symbol, expr)
    self.system.facts[symbol] = expr

  def extract(self):
    expr = self.copy()
    expr.simplify()
    terms = expr.terms
    if len(terms) == 0:
      return 0
    assert len(terms) == 1
    return terms[None]

  def __iadd__(self, other):
    other = self._to_expr(other)
    for s, x in other.terms.items():
      self._set(s, self.terms.get(s, 0) + x)
    return self

  def __imul__(self, val):
    items = self.terms.items()
    self.terms = {}
    for s, x in items:
      self._set(s, x * val)
    return self

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
    return str(self)
