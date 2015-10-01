import boxes

box1 = boxes.Box(aspect=1)
box2 = boxes.Box(aspect=1)

fig = boxes.Box(width=6.0)
fig.pad(0.2).fix(boxes.row(box1, box2, spacing=0.5))

fig.solve()

if __name__ == '__main__':
  import sys
  from boxes.display import display
  display(sys.argv[1], fig, (box1, box2))
