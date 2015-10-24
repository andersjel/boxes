def format(terms):
  terms = list(terms)
  if len(terms) == 0:
    return "0"

  acc = ""

  first = True
  for symbol, val in terms:
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
