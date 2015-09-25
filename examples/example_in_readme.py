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
grid.solve()

print('The size of the figure is {:.2f} × {:.2f}.'.format(*grid.size))
print('box3 is located at ({:.2f}, {:.2f}).'.format(*box3.loc))

if __name__ == '__main__':
  import sys
  from boxes.display import display
  display(sys.argv[1], (box1, box2, box3))
