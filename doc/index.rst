The boxes library
=================

The purpose of the boxes library is to align rectangles in 2D based on fairly
general *constraints*. For instance, it can be used to make sub-plots in a
figure line up nicely, with easy control over margins and dimensions.

.. image:: /../examples/example1.*

Here is an example of a problem of this kind (illustrated above): Suppose two
squares are next to each other with 0.3 units of spacing between them, in a
figure with margins of 0.3 units and a total width of 6.0 units. How tall is
this figure? The answer is (6.0 − 0.3 × 3) / 2 + 0.3 × 2 = 3.15. Clearly, as
figures become more complicated, solving these kinds of problems by hand quickly
gets complicated. This is where this library comes in.

Below is code solving the above example::

  import boxes

  ctx = boxes.Context()

  # Create two squares
  square1 = ctx.box(aspect=1)
  square2 = ctx.box(aspect=1)

  # Put them next to each other
  row = boxes.constrain.row(square1, square2, spacing=0.3)

  # Create a box representing the figure
  fig = ctx.box(width=6.0)
  # And insert row with 0.3 units of padding
  fig.pad(0.3).fix(row)

  fig.solve()
  print(fig.height)  # prints 3.15

.. toctree::
  :caption: The boxes package
  :maxdepth: 2

  boxes-intro
  new-constraints
  boxes-reference

.. toctree::
  :caption: The symmath package
  :maxdepth: 2

  symmath-intro
  symmath-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
