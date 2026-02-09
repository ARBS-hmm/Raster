from manim import *

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

def flood(grid, scene, x, y, boundary, delay=0.5):
    start_color = get_pixel_color(grid, x, y)
    if start_color is None or start_color == boundary or start_color == BLUE:
        return
    
    stack = [(x, y)]
    while stack:
        current_x, current_y = stack.pop()
        
        if current_x < 0 or current_x >= rows or current_y < 0 or current_y >= cols:
            continue
        
        index = current_x * cols + current_y
        current_color = grid[index].get_fill_color()
        
        if current_color == BLUE: 
            continue
            
        if current_color == boundary:
            # FIXED: Added grid parameter
            set_pixel(grid, current_x, current_y, RED)
            scene.wait(delay)
            set_pixel(grid, current_x, current_y, WHITE)
            continue

        
        # Skip if not the same color as starting point
        if current_color != start_color:
            continue
        
        # Fill this pixel
        set_pixel(grid, current_x, current_y, color=BLUE)
        
        # Add configurable delay
        scene.wait(delay)
        
        # Add neighbors to stack (4-directional)
        stack.append((current_x + 1, current_y))
        stack.append((current_x - 1, current_y))
        stack.append((current_x, current_y + 1))
        stack.append((current_x, current_y - 1))

class Flood(Scene):
    def construct(self):
        grid = VGroup()
        pixel = 0.2
        
        # Create pixel grid
        for i in range(rows):
            for j in range(cols):
                grid.add(
                    Square(pixel)
                    .set_stroke(color=WHITE, opacity=1, width=0.5)
                    .move_to([i * pixel, j * pixel, 0.0])
                    .set_fill(color=BLACK, opacity=1)  # Start with black background
                )

        # Keep your exact code display part
        code = VGroup()
        PREFIX = "●"  # forces spaces to be non-leading
        lines = [
            "test",
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

        # Draw a rectangle boundary
        rectangle(grid, 10, 1, 20, 10)
        self.wait(1)
        
        # Perform flood fill
        flood(grid, self, 13, 3, WHITE)
        
        self.wait(10)
