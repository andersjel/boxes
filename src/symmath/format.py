def join_terms(terms):
  if len(terms) == 0:
    return "0"
  rval = ""
  first = True
  for sign, factors in terms:
    if first:
      if sign != '+':
        rval += sign
      first = False
    else:
      rval += " {} ".format(sign)
    if not factors:
      rval += "1"
    else:
      rval += " ".join(factors)
  return rval


def format_scalar(scalar):
  if isinstance(scalar, complex):
    # TODO  handle this better.
    return '+', ["({})".format(scalar)]
  if scalar < 0:
    sign = '-'
    scalar *= -1
  else:
    sign = '+'
  s = str(scalar)
  if s == '1':
    return sign, []
  else:
    return sign, [s]


def format(expr):
  terms = []

  for symbol, value in expr.terms.items():
    if symbol is None:
      continue
    sign, scalar = format_scalar(value)
    if isinstance(symbol, int):
      sym = "x" + str(symbol)
    else:
      sym = str(symbol)
    terms.append((sign, scalar + [sym]))

  terms.sort(key=lambda x: x[1][-1])

  if expr[None] != 0:
    terms.append(format_scalar(expr[None]))

  return join_terms(terms)
