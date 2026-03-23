from manim import *
from Grid import Grid

rows, cols = 70, 30

def set_pixel(grid, i, j, cols, color=WHITE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def draw_circle_pixels(grid, scene, code_lines, xc, yc, x, y):
    """Draw all 8 symmetric pixels for a circle with individual highlighting"""
    
    # Define all 8 pixel positions with their corresponding code lines
    pixel_positions = [
        (xc + x, yc + y, 4),   # putpixel(xc + x, yc + y)
        (xc - x, yc + y, 5),   # putpixel(xc - x, yc + y)
        (xc + x, yc - y, 6),   # putpixel(xc + x, yc - y)
        (xc - x, yc - y, 7),   # putpixel(xc - x, yc - y)
        (xc + y, yc + x, 8),   # putpixel(xc + y, yc + x)
        (xc - y, yc + x, 9),   # putpixel(xc - y, yc + x)
        (xc + y, yc - x, 10),  # putpixel(xc + y, yc - x)
        (xc - y, yc - x, 11),  # putpixel(xc - y, yc - x)
    ]
    
    for px, py, line_num in pixel_positions:
        # Highlight the specific line for this pixel
        scene.highlight_code_line(code_lines, line_num)
        set_pixel(grid, px, py, cols, color=BLUE, opacity=1)
        scene.wait(0.2)  # Small delay to see each pixel being placed

def midpoint_circle(scene, code_lines, grid, xc, yc, r):
    """Implement midpoint circle algorithm with visualization"""
    x = 0
    y = r
    d = 1 - r  # Initial decision parameter
    
    # Create large P value display at bottom center
    p_display = Text(f"P = {d}", font="Monospace", font_size=36, color=GREEN, weight=BOLD)
    p_display.to_edge(DOWN, buff=0.8)
    scene.add(p_display)
    
    # Create small x and y display below P (or above, whichever looks better)
    xy_display = Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE)
    xy_display.next_to(p_display, UP, buff=0.3)
    scene.add(xy_display)
    
    while x <= y:
        # Highlight while loop condition
        scene.highlight_code_line(code_lines, 3)
        scene.wait(0.3)
        
        # Draw all 8 symmetric pixels with individual highlighting
        scene.highlight_code_line(code_lines, 4)  # First pixel line to start
        draw_circle_pixels(grid, scene, code_lines, xc, yc, x, y)
        
        # Update displays
        p_display.become(Text(f"P = {d}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
        p_display.to_edge(DOWN, buff=0.8)
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        
        # Check decision parameter (no text display, just highlight)
        scene.highlight_code_line(code_lines, 12)
        scene.wait(0.6)
        
        if d < 0:
            scene.highlight_code_line(code_lines, 13)
            d += 2 * x + 3
            scene.wait(0.5)
        else:
            scene.highlight_code_line(code_lines, 15)
            d += 2 * (x - y) + 5
            scene.wait(0.4)
            
            scene.highlight_code_line(code_lines, 16)
            y -= 1
            scene.wait(0.5)
        
        scene.highlight_code_line(code_lines, 18)
        x += 1
        scene.wait(0.5)
    
    scene.wait(2)

class GridCircle(Scene):
    def highlight_code_line(self, code_lines, line_number):
        """Highlight a specific line in the code block"""
        for i, line in enumerate(code_lines, start=1):
            line.set_color(YELLOW if i == line_number else WHITE)
            line.set_opacity(1 if i == line_number else 0.5)
    
    def construct(self):
        # Create grid using Grid library
        grid = Grid(rows, cols)
        
        # Create code block
        code = VGroup()
        
        PREFIX = "●"  # forces spaces to be non-leading
        lines = [
            "void circle(int xc, int yc, int r) {",                    #1
            "   int x = 0, y = r, d = 1 - r;",                        #2
            "   while (x <= y) {",                                    #3
            "      putpixel(xc + x, yc + y);",                        #4
            "      putpixel(xc - x, yc + y);",                        #5
            "      putpixel(xc + x, yc - y);",                        #6
            "      putpixel(xc - x, yc - y);",                        #7
            "      putpixel(xc + y, yc + x);",                        #8
            "      putpixel(xc - y, yc + x);",                        #9
            "      putpixel(xc + y, yc - x);",                        #10
            "      putpixel(xc - y, yc - x);",                        #11
            "      if (d < 0) {",                                     #12
            "         d += 2 * x + 3;",                               #13
            "      } else {",                                         #14
            "         d += 2 * (x - y) + 5;",                         #15
            "         y--;",                                          #16
            "      }",                                                #17
            "      x++;",                                             #18
            "   }",                                                   #19
            "}",                                                      #20
        ]
        
        for line in lines:
            text = Text(
                PREFIX + line,
                font="Monospace",
                font_size=9,
                color=WHITE
            )
            # hide the prefix so indentation works
            text[0].set_opacity(0)
            code.add(text)
        
        # Arrange lines with perfect left alignment
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code.to_edge(LEFT).to_edge(UP, buff=0.5)
        
        # Add grid and code to scene
        self.add(grid, code)
        self.wait(2)
        
        # Run the circle algorithm with center at (6, 6) and radius 5
        midpoint_circle(self, code, grid, 6, 6, 5)
        
        self.wait(5)
