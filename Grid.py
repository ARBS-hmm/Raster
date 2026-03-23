from manim import *

def Grid(rows, cols):
    grid = VGroup()
    pixel = 0.2
    for i in range(rows):
        for j in range(cols):
            grid.add(
                Square(pixel)
                .set_stroke(color=WHITE, opacity=1, width=0.5)
                .move_to([i * pixel, j * pixel, 0.0])
            )
    return grid  # Add this line to return the grid
