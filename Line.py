from manim import *
from Grid import Grid

rows, cols = 70, 20

def set_pixel(grid, i, j, cols, color=BLUE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def bresenham(grid, scene, code_lines, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    P = 2*dy - dx
    
    # Create large P value display at bottom center
    p_display = Text(f"P = {P}", font="Monospace", font_size=36, color=GREEN, weight=BOLD)
    p_display.to_edge(DOWN, buff=0.8)
    scene.add(p_display)
    
    # Create small x and y display above P
    xy_display = Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE)
    xy_display.next_to(p_display, UP, buff=0.3)
    scene.add(xy_display)
    
    while x != x1:
        # Draw pixel
        scene.highlight_code_line(code_lines, 8)
        set_pixel(grid, x, y, cols)
        
        # Update displays
        p_display.become(Text(f"P = {P}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
        p_display.to_edge(DOWN, buff=0.8)
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        scene.wait(0.5)
        
        # Check condition (no text display, just highlight)
        scene.highlight_code_line(code_lines, 9)
        scene.wait(0.6)
        
        if P < 0:
            scene.highlight_code_line(code_lines, 10)
            P += 2*dy
            scene.wait(0.5)
        else:
            scene.highlight_code_line(code_lines, 12)
            y += 1
            scene.wait(0.4)
            
            scene.highlight_code_line(code_lines, 13)
            P += 2*dy - 2*dx
            scene.wait(0.5)
        
        scene.highlight_code_line(code_lines, 14)
        x += 1
        scene.wait(0.5)
    
    scene.wait(1)

class GridLine(Scene):
    def highlight_code_line(self, code_lines, line_number):
        for i, line in enumerate(code_lines, start=1):
            line.set_color(YELLOW if i == line_number else WHITE)
            line.set_opacity(1 if i == line_number else 0.5)
    
    def construct(self):
        grid = Grid(rows, cols)
        
        code = VGroup()
        lines = [
            "void bresenham(int x0, int y0, int x1, int y1) {",
            "   int dx = x1 - x0;",
            "   int dy = y1 - y0;",
            "   int x = x0;",
            "   int y = y0;",
            "   int P = 2*dy - dx;",
            "   while (x != x1) {",
            "      putpixel(x, y);",
            "      if (P < 0)",
            "         P += 2*dy;",
            "      else",
            "         y++;",
            "         P += 2*dy - 2*dx;",
            "      x++;",
            "   }",
            "}",
        ]
        
        for line in lines:
            text = Text("●" + line, font="Monospace", font_size=9, color=WHITE)
            text[0].set_opacity(0)
            code.add(text)
        
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code.to_edge(LEFT).to_edge(UP, buff=0.5)
        
        self.add(grid, code)
        self.wait(2)
        
        bresenham(grid, self, code, 1, 1, 40, 20)
        self.wait(5)
