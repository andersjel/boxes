Introduction to symmath
=======================

Expressions of type :class:`~symmath.expr.Expr` emulate numeric types to some
extent. Specifically, only linear combinations of symbols are supported.

>>> from symmath import Expr, sym
>>> a = sym('a')
>>> b = sym('b')
>>> a + b
Expr(a + b)
>>> 2 * (3 * a + b + 2)
Expr(6 a + 2 b + 4)
>>> a * b
Traceback (most recent call last):
  ...
TypeError: ...

To convert an expression to a regular number, use
:func:`symmath.expr.Expr.scalar()`, which throws an exception if an expression
contains symbols (which obviously cannot be converted).

>>> x = a + 3
>>> (x - a).scalar()
3
>>> (x - b).scalar()
Traceback (most recent call last):
  ...
AssertionError: ...

Expressions can be copied and modified in place.

>>> x = Expr(a)
>>> x is not a
True
>>> x += 2 * b
>>> x
Expr(a + 2 b)
>>> a
Expr(a)

The coeffient in front of each term can be accessed and modified using item
accessors.

>>> x = 1.5 * a + b
>>> x['a']
1.5
>>> x['a'] += 3
>>> x
Expr(4.5 a + b)
>>> del x['a']
>>> x['c'] = 2
>>> x
Expr(b + 2 c)
>>> x['d']
0

As a special case, *None* can be used to access the scalar part of an
expression.

>>> x = a + b + 3
>>> x[None]
3
>>> x[None] = 4
>>> x
Expr(a + b + 4)

Any object than can be used as key in a dictionary can be used to name a symbol
(note, integers get an 'x' prefixed when printing).

>>> x = sym(('x', 'y')) + sym(3) + sym(1) + 3
>>> x
Expr(('x', 'y') + x1 + x3 + 3)
