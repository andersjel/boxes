import boxes

box1 = boxes.Box(aspect=1)   # a square box of any size
box2 = boxes.Box(width=1.5)  # a 1.5 unit wide box
box3 = boxes.Box(height=1.0) # a 1.0 unit tall box

grid = boxes.Grid(2, 2)      # a two-by-two grid
grid[0, 0].fix(box1)         # put box1 in the top left corner
grid[:, 1].fix(box2)         # put box2 across the two cells on the right
grid[1, 0].fix(box3)         # put box3 in the bottom left corner
grid[:, :].spacing(0.4)      # set spacings everywhere in the grid to 0.4 units

fig = boxes.Box(width=6.0)   # a 6 unit wide box to represent the figure
fig.pad(0.2).fix(grid)       # put the grid in the figure with 0.2 unit margins
fig.solve()                  # Solve the layout
# TODO remove this:
fig.layout.equate(fig.left, 0)
fig.layout.equate(fig.top, 0)

print('The size of the figure is {:.2f} × {:.2f}.'.format(*fig.size))
print('box3 is located at ({:.2f}, {:.2f}).'.format(*box3.loc))

if __name__ == '__main__':
  import sys
  from boxes.display import display
  display(sys.argv[1], fig, (box1, box2, box3))
