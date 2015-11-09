The boxes library
=================

The purpose of the boxes library is to align rectangles in 2D based on fairly
general *constraints*. For instance, it can be used to make sub-plots in a
figure line up nicely, with easy control over margins and dimensions.

.. image:: /figures/index.*

The illustration above shows an example of this kind: The figure is 6 units wide
and contains a square and a rectangle twice as wide; all spacings are 0.3 units.
How heigh should the figure be? — The answer is (6.0 − 0.3 × 3) / 3 + 0.3 × 2 =
2.3. Clearly, as figures become more complicated, solving these kinds of
problems by hand quickly gets complicated. This is where this library comes in.

Below is code solving the above example:

.. testcode::

  from boxes import Context, constrain

  ctx = Context()

  # A box representing the figure. We only define its width.
  fig = ctx.box(width=6)

  # Create a square of any size, and a rectangle twice as wide
  square = ctx.box(aspect=1)
  rectangle = ctx.box(width=2 * square.width)

  # Align the square and rectangle next to each other.
  row = constrain.row(square, rectangle, spacing=0.3)

  # Put them in the figure with 0.3 units of margins.
  fig.pad(0.3).fix(row)

  fig.solve()
  print("The height of the figure is", fig.height)

.. testoutput::

  The height of the figure is 2.3

.. testcode::
  :hide:

  from boxes.display import display
  display("figures/index.svg", fig, (square, rectangle))

This library supports any constraint which can ulitmately be expressed as a set
of linear equations. See the :doc:`boxes/constrain` module for some examples.

.. toctree::
  :caption: The boxes package
  :maxdepth: 2

  boxes-intro
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
