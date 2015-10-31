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

if __name__ == '__main__':
  import sys
  from boxes.display import display
  display(sys.argv[1], fig, (square1, square2))
