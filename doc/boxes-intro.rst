Introduction to boxes
=====================

The central class in this library is the :class:`~boxes.box.Box` class. To get
hold of one, first construct a :class:`~boxes.context.Context`.

>>> from boxes import Context
>>> ctx = Context()
>>> box1 = ctx.box()

A :class:`~boxes.box.Box` has two main properties, a location and a size.

>>> print(box1.loc)
(x3, x0)
>>> print(box1.size)
(x1 - x3, -x0 + x2)

Note that these are symbolic expressions. Constraints in the *boxes* library are
handled internally by adding equations to the context. Let us try creating a
constraint, by creating second box and putting the two boxes next to each other
with some spacing between them using :func:`boxes.constrain.row`.

>>> from boxes import constrain
>>> box2 = ctx.box()
>>> fig = constrain.row(box1, box2, spacing=0.3)

We have now added some equations to the context.

>>> len(ctx.system.facts) > 0
True

But we have not added enough to completely define the layout, therefore calling
:func:`~boxes.box.Box.solve` on *fig* (which is the bounding box of *box1* and
*box2*) raises an exception.

>>> fig.solve()
Traceback (most recent call last):
  ...
AssertionError

Lets add a few more constraints until the system is completely defined. First,
let us set the total size.

>>> constrain.size((6, 2), fig)

And now let us set *box1* to be twice as wide as *box2* is tall.

>>> ctx.equate(box1.width, 2 * box2.height)

That should do it, now we have enough equations.

>>> fig.solve()

After calling ``fig.solve()``, properties that were symbolic before are now
regular floats:

>>> print(box1.loc)
(0.0, 0.0)
>>> print(box1.size)
(4.0, 2.0)

Let us have a look at the output

>>> from boxes.display import display
>>> display("figures/intro.svg", fig, (box1, box2))

.. image:: /figures/intro.*
