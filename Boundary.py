from manim import *
from Stacklib import *

rows, cols = 70, 30

def set_pixel(grid, i, j, color=WHITE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def rectangle(grid, x1, y1, x2, y2):
    print("rectangle")
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
        return grid[index].get_fill_color()
    return None

def boundaryfill(grid, scene, x, y, boundary, delay=0.5):
    start_color = get_pixel_color(grid, x, y)
    if start_color is None or start_color == boundary or start_color == BLUE:
        return

    # Create stack with same dimensions as StackDemo
    stack = ManimStack(
        box_width=2.5,
        box_height=0.4,
        box_corner_radius=0.1,
        box_buff=0.1,
        font_size=14,
        max_visible=5,
        stack_center=DOWN * 3 + LEFT * 5  # Position to right of grid
    )
    
    # Make the stack
    stack_vgroup = stack.make_stack(initial_count=5)
    scene.add(stack_vgroup)
    stack.set_scene(scene)
    
    # Initialize stack with starting pixel
    stack.add_element(f"({x},{y})")
    stack_list = [(x, y)]
    
    while stack_list:
        # Pop from both the logic stack and visual stack
        current_x, current_y = stack_list.pop()
        stack.pop_element()
        
        if current_x < 0 or current_x >= rows or current_y < 0 or current_y >= cols:
            continue
        
        current_color = get_pixel_color(grid, current_x, current_y)
        
        # Handle boundary hits
        if current_color == BLUE:
            set_pixel(grid, current_x, current_y, RED)
            scene.wait(delay)
            set_pixel(grid, current_x, current_y, BLUE)
            continue
            
        if current_color == boundary:
            set_pixel(grid, current_x, current_y, RED)
            scene.wait(delay)
            set_pixel(grid, current_x, current_y, boundary)
            continue

        # Skip if not the start color
        if current_color != start_color:
            continue
        
        # FILL ANIMATION FIRST - change pixel to BLUE
        set_pixel(grid, current_x, current_y, color=BLUE)
        scene.wait(delay)
        
        # THEN update stack visualization with neighbors
        neighbors = [
            (current_x + 1, current_y),
            (current_x - 1, current_y),
            (current_x, current_y + 1),
            (current_x, current_y - 1)
        ]
        
        # Add neighbors to stack (reverse order for desired processing order)
        for nx, ny in reversed(neighbors):
            # Check bounds before adding to stack
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbor_color = get_pixel_color(grid, nx, ny)
                # Only add if it's the start color and not a boundary
                if neighbor_color == start_color:
                    coord_str = f"({nx},{ny})"
                    stack.add_element(coord_str)
                    stack_list.append((nx, ny))
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

        # Display C++ graphics.h flood-fill code
        code = VGroup()
        PREFIX = "●"  # forces spaces to be non-leading
        lines = [
            "void boundaryFill(int x, int y, int boundaryColor, int fillColor){",
            "    int currentColor = getpixel(x, y);",
            "",
            "    if (currentColor==boundaryColor||currentColor==fillColor)",
            "        return;",
            "",
            "    putpixel(x, y, fillColor);",
            "",
            "    floodFill(x + 1, y, boundaryColor, fillColor);",
            "    floodFill(x - 1, y, boundaryColor, fillColor);",
            "    floodFill(x, y + 1, boundaryColor, fillColor);",
            "    floodFill(x, y - 1, boundaryColor, fillColor);",
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

       # rectangle(grid, 13, 3, 16, 6)
       # boundaryfill(grid, self, 14, 4, WHITE)

        rectangle(grid, 0, 0, 5, 4)
        boundaryfill(grid, self, 2, 2, BLUE)  # or any color you prefer
       # rectangle(grid, 0, 0, 5, 4)
       # boundaryfill(grid, self, 2, 2, GREEN)  # or any color you prefer

        self.wait(5)
