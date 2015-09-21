import boxes

grid = boxes.Grid(2, 2, width=6.0)  # a two-by-two grid, 6 units wide
box1 = boxes.Box(aspect=1)          # a square box of any size
box2 = boxes.Box(width=1.5)         # a 1.5 unit wide box
box3 = boxes.Box(height=1.0)        # a 1.0 unit tall box

grid[0, 0].fix(box1)     # put box1 in the top left corner
grid[:, 1].fix(box2)     # put box2 across the two cells on the right
grid[1, 0].fix(box3)     # put box3 in the bottom left corner

grid[:, :].spacing(0.4)  # set spacings everywhere in the grid to 0.4 units
grid.margins(all=0.2)    # Set margins outside the grid to 0.2 units

# Solve the layout
sls = grid.solve()

total_size = sls.eval(grid.size)
print('The size of the figure is {:.2f} × {:.2f}.'.format(*total_size))
box3_loc = sls.eval(box3.loc)
print('box3 is located at ({:.2f}, {:.2f}).'.format(*box3_loc))

if __name__ == '__main__':
  import cairo
  import sys
  output_filename, = sys.argv[1:]
  dots_per_unit = 30
  width, height = (int(x * dots_per_unit + 0.5) for x in total_size)
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  ctx = cairo.Context(surf)
  ctx.scale(dots_per_unit, dots_per_unit)
  ctx.set_source_rgb(0.8, 0.8, 0.8)
  ctx.paint()
  ctx.set_source_rgb(0.4, 0.4, 0.4)
  for box in (box1, box2, box3):
    x, y = sls.eval(box.loc)
    w, h = sls.eval(box.size)
    ctx.rectangle(x, y, w, h)
  ctx.fill()
  surf.write_to_png(output_filename)
