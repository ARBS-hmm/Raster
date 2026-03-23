from manim import *
from Stacklib import *

rows, cols = 70, 30

def set_pixel(grid, i, j, color=WHITE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def rectangle(grid, x1, y1, x2, y2):
    # Top edge
    for x in range(x1, x2 + 1):
        set_pixel(grid, x, y1)
    # Bottom edge
    for x in range(x1, x2 + 1):
        set_pixel(grid, x, y2)
    # Left edge
    for y in range(y1, y2 + 1):
        set_pixel(grid, x1, y)
    # Right edge
    for y in range(y1, y2 + 1):
        set_pixel(grid, x2, y)

def get_pixel_color(grid, i, j):
    if 0 <= i < rows and 0 <= j < cols:
        index = i * cols + j
        return grid[index].get_fill_color().to_hex().upper()
    return None

def color_to_hex(color):
    """Convert a manim color constant to uppercase hex string for reliable comparison."""
    return ManimColor(color).to_hex().upper()

def boundaryfill(grid, scene, x, y, boundary_color, fill_color=BLUE, delay=0.3):
    boundary_hex = color_to_hex(boundary_color)
    fill_hex     = color_to_hex(fill_color)

    start_hex = get_pixel_color(grid, x, y)
    # Don't fill if starting on boundary or already filled
    if start_hex is None or start_hex == boundary_hex or start_hex == fill_hex:
        return

    # Create visual stack — start empty
    stack = ManimStack(
        box_width=2.5,
        box_height=0.4,
        box_corner_radius=0.1,
        box_buff=0.1,
        font_size=14,
        max_visible=5,
        stack_center=DOWN * 3 + LEFT * 5
    )
    stack_vgroup = stack.make_stack(initial_count=0)
    scene.add(stack_vgroup)
    stack.set_scene(scene)

    # Seed both the logic stack and the visual stack
    logic_stack = [(x, y)]
    stack.add_element(f"({x},{y})")

    while logic_stack:
        current_x, current_y = logic_stack.pop()
        stack.pop_element()                          # visual pop always matches logic pop

        # Out-of-bounds guard
        if not (0 <= current_x < rows and 0 <= current_y < cols):
            continue

        current_hex = get_pixel_color(grid, current_x, current_y)

        # Skip boundary pixels
        if current_hex == boundary_hex:
            continue

        # Skip already-filled pixels
        if current_hex == fill_hex:
            continue

        # Skip pixels that are not the interior colour
        if current_hex != start_hex:
            continue

        # Fill this pixel
        set_pixel(grid, current_x, current_y, color=fill_color)
        scene.wait(delay)

        # Push valid (unfilled, non-boundary, in-bounds) neighbours
        neighbors = [
            (current_x + 1, current_y),
            (current_x - 1, current_y),
            (current_x,     current_y + 1),
            (current_x,     current_y - 1),
        ]

        # Reverse so the first neighbour ends up on top of the stack
        for nx, ny in reversed(neighbors):
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue
            nhex = get_pixel_color(grid, nx, ny)
            if nhex != boundary_hex and nhex != fill_hex and nhex == start_hex:
                logic_stack.append((nx, ny))
                stack.add_element(f"({nx},{ny})")


class Boundary(Scene):
    def construct(self):
        grid = VGroup()
        pixelwidth = 0.2

        # Create pixel grid
        for i in range(rows):
            for j in range(cols):
                grid.add(
                    Square(pixelwidth)
                    .set_stroke(color=WHITE, opacity=1, width=0.5)
                    .move_to([i * pixelwidth, j * pixelwidth, 0])
                    .set_fill(color=BLACK, opacity=1)
                )

        # Display boundary-fill pseudocode
        code = VGroup()
        PREFIX = "●"
        lines = [
            "void boundaryFill(x, y, boundaryColor, fillColor) {",
            "    color = getpixel(x, y);",
            "    if (color == boundaryColor || color == fillColor)",
            "        return;",
            "    putpixel(x, y, fillColor);",
            "    boundaryFill(x+1, y, boundaryColor, fillColor);",
            "    boundaryFill(x-1, y, boundaryColor, fillColor);",
            "    boundaryFill(x, y+1, boundaryColor, fillColor);",
            "    boundaryFill(x, y-1, boundaryColor, fillColor);",
            "}",
        ]

        for line in lines:
            text = Text(
                PREFIX + line,
                font="Monospace",
                font_size=9,
                color=WHITE
            )
            text[0].set_opacity(0)
            code.add(text)

        code.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code.to_edge(LEFT).to_edge(UP, buff=0.5)

        self.add(grid)
        self.add(code)

        # Draw a WHITE rectangle, then fill its BLACK interior with BLUE
        rectangle(grid, 0, 0, 5, 4)
        boundaryfill(grid, self, 2, 2, boundary_color=WHITE, fill_color=BLUE)

        self.wait(5)