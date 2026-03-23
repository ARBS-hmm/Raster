from manim import *
from Grid import Grid

rows, cols = 70, 40

def set_pixel(grid, i, j, cols, color=WHITE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def draw_ellipse_pixels(grid, xc, yc, x, y):
    """Draw all 4 symmetric pixels for an ellipse"""
    set_pixel(grid, xc + x, yc + y, cols)
    set_pixel(grid, xc - x, yc + y, cols)
    set_pixel(grid, xc + x, yc - y, cols)
    set_pixel(grid, xc - x, yc - y, cols)

def show_code(scene, lines, title):
    """Create and display code block"""
    code = VGroup()
    for line in lines:
        text = Text("●" + line, font="Monospace", font_size=9, color=WHITE)
        text[0].set_opacity(0)
        code.add(text)
    code.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    code.to_edge(LEFT).to_edge(UP, buff=0.5)
    
    title_text = Text(title, font="Monospace", font_size=12, color=GREEN)
    title_text.next_to(code, DOWN, buff=0.2)
    title_text.align_to(code, LEFT)
    
    scene.add(code, title_text)
    return code, title_text

def highlight_line(scene, code_lines, line_num):
    """Highlight specific line"""
    for i, line in enumerate(code_lines, start=1):
        line.set_color(YELLOW if i == line_num else WHITE)
        line.set_opacity(1 if i == line_num else 0.5)

def region1_algorithm(scene, grid, xc, yc, rx, ry):
    """Region 1 of ellipse algorithm"""
    # Region 1 code
    region1_lines = [
        "void ellipse(int xc, int yc, int rx, int ry) {",
        "   // Region 1: dx < dy",
        "   int x = 0, y = ry;",
        "   int rx_sq = rx * rx;",
        "   int ry_sq = ry * ry;",
        "   int d1 = ry_sq - (rx_sq * ry) + (0.25 * rx_sq);",
        "   ",
        "   while ((2 * ry_sq * x) < (2 * rx_sq * y)) {",
        "      putpixel(xc + x, yc + y);",
        "      if (d1 < 0) {",
        "         d1 += (2 * ry_sq * x) + (2 * ry_sq) + ry_sq;",
        "      } else {",
        "         y--;",
        "         d1 += (2 * ry_sq * x) - (2 * rx_sq * y) + (2 * ry_sq) + (3 * rx_sq) + ry_sq;",
        "      }",
        "      x++;",
        "   }",
        "}"
    ]
    
    code, title = show_code(scene, region1_lines, "Region 1: Slope < 1")
    
    x = 0
    y = ry
    rx_sq = rx * rx
    ry_sq = ry * ry
    d1 = ry_sq - (rx_sq * ry) + (0.25 * rx_sq)
    
    # Create P value display at bottom left
    p_display = Text(f"P = {d1:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD)
    p_display.to_edge(DOWN + LEFT, buff=0.8)
    scene.add(p_display)
    
    xy_display = Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE)
    xy_display.next_to(p_display, UP, buff=0.3)
    xy_display.align_to(p_display, LEFT)
    scene.add(xy_display)
    
    scene.wait(1)
    
    while (2 * ry_sq * x) < (2 * rx_sq * y):
        # Draw pixel
        highlight_line(scene, code, 9)
        draw_ellipse_pixels(grid, xc, yc, x, y)
        scene.wait(0.2)
        
        # Update displays
        p_display.become(Text(f"P = {d1:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD))
        p_display.to_edge(DOWN + LEFT, buff=0.8)
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        xy_display.align_to(p_display, LEFT)
        
        # Check condition
        highlight_line(scene, code, 10)
        cond_text = Text(f"d1 < 0? {d1:.1f} < 0", font="Monospace", font_size=14, color=YELLOW)
        cond_text.next_to(xy_display, UP, buff=0.3)
        cond_text.align_to(p_display, LEFT)
        scene.add(cond_text)
        scene.wait(0.5)
        
        if d1 < 0:
            highlight_line(scene, code, 11)
            old_d = d1
            addition = Text(f"P = {old_d:.1f} + (2*{x}*ry_sq + 2*ry_sq + ry_sq)",
                          font="Monospace", font_size=10, color=YELLOW)
            addition.next_to(cond_text, UP, buff=0.2)
            addition.align_to(p_display, LEFT)
            scene.add(addition)
            scene.wait(0.4)
            
            d1 += (2 * ry_sq * x) + (2 * ry_sq) + ry_sq
            
            p_display.become(Text(f"P = {d1:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)
            scene.remove(addition)
        else:
            highlight_line(scene, code, 13)
            old_y = y
            y_decrement = Text(f"y = {old_y} - 1 = {old_y - 1}",
                             font="Monospace", font_size=10, color=YELLOW)
            y_decrement.next_to(cond_text, UP, buff=0.2)
            y_decrement.align_to(p_display, LEFT)
            scene.add(y_decrement)
            scene.wait(0.3)
            
            y -= 1
            
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.3)
            scene.remove(y_decrement)
            
            highlight_line(scene, code, 14)
            old_d = d1
            addition = Text(f"P = {old_d:.1f} + (2*ry_sq*x - 2*rx_sq*y + 2*ry_sq + 3*rx_sq + ry_sq)",
                          font="Monospace", font_size=9, color=YELLOW)
            addition.next_to(cond_text, UP, buff=0.2)
            addition.align_to(p_display, LEFT)
            scene.add(addition)
            scene.wait(0.4)
            
            d1 += (2 * ry_sq * x) - (2 * rx_sq * y) + (2 * ry_sq) + (3 * rx_sq) + ry_sq
            
            p_display.become(Text(f"P = {d1:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)
            scene.remove(addition)
        
        scene.remove(cond_text)
        highlight_line(scene, code, 16)
        x += 1
        
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        xy_display.align_to(p_display, LEFT)
        scene.wait(0.3)
    
    scene.remove(code, title)
    return x, y, rx_sq, ry_sq

def region2_algorithm(scene, grid, xc, yc, rx, ry, x, y, rx_sq, ry_sq):
    """Region 2 of ellipse algorithm"""
    # Region 2 code
    region2_lines = [
        "void ellipse(int xc, int yc, int rx, int ry) {",
        "   // Region 2: dx > dy",
        "   int d2 = ry_sq * (x + 0.5) * (x + 0.5) + rx_sq * (y - 1) * (y - 1) - rx_sq * ry_sq;",
        "   ",
        "   while (y >= 0) {",
        "      putpixel(xc + x, yc + y);",
        "      if (d2 < 0) {",
        "         x++;",
        "         d2 += (2 * ry_sq * x) - (2 * rx_sq * y) + (3 * ry_sq) + rx_sq;",
        "      } else {",
        "         y--;",
        "         d2 += (2 * rx_sq) - (2 * rx_sq * y) + (2 * ry_sq * x) + (3 * ry_sq) + rx_sq;",
        "      }",
        "   }",
        "}"
    ]
    
    code, title = show_code(scene, region2_lines, "Region 2: Slope > 1")
    
    # Calculate initial d2 for region 2
    d2 = ry_sq * (x + 0.5) * (x + 0.5) + rx_sq * (y - 1) * (y - 1) - rx_sq * ry_sq
    
    # Create P value display at bottom left
    p_display = Text(f"P = {d2:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD)
    p_display.to_edge(DOWN + LEFT, buff=0.8)
    scene.add(p_display)
    
    xy_display = Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE)
    xy_display.next_to(p_display, UP, buff=0.3)
    xy_display.align_to(p_display, LEFT)
    scene.add(xy_display)
    
    scene.wait(1)
    
    while y >= 0:
        # Draw pixel
        highlight_line(scene, code, 6)
        draw_ellipse_pixels(grid, xc, yc, x, y)
        scene.wait(0.2)
        
        # Update displays
        p_display.become(Text(f"P = {d2:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD))
        p_display.to_edge(DOWN + LEFT, buff=0.8)
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        xy_display.align_to(p_display, LEFT)
        
        # Check condition
        highlight_line(scene, code, 7)
        cond_text = Text(f"d2 < 0? {d2:.1f} < 0", font="Monospace", font_size=14, color=YELLOW)
        cond_text.next_to(xy_display, UP, buff=0.3)
        cond_text.align_to(p_display, LEFT)
        scene.add(cond_text)
        scene.wait(0.5)
        
        if d2 < 0:
            highlight_line(scene, code, 8)
            old_x = x
            x_increment = Text(f"x = {old_x} + 1 = {old_x + 1}",
                             font="Monospace", font_size=10, color=YELLOW)
            x_increment.next_to(cond_text, UP, buff=0.2)
            x_increment.align_to(p_display, LEFT)
            scene.add(x_increment)
            scene.wait(0.3)
            
            x += 1
            
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.3)
            scene.remove(x_increment)
            
            highlight_line(scene, code, 9)
            old_d = d2
            addition = Text(f"P = {old_d:.1f} + (2*ry_sq*x - 2*rx_sq*y + 3*ry_sq + rx_sq)",
                          font="Monospace", font_size=9, color=YELLOW)
            addition.next_to(cond_text, UP, buff=0.2)
            addition.align_to(p_display, LEFT)
            scene.add(addition)
            scene.wait(0.4)
            
            d2 += (2 * ry_sq * x) - (2 * rx_sq * y) + (3 * ry_sq) + rx_sq
            
            p_display.become(Text(f"P = {d2:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)
            scene.remove(addition)
        else:
            highlight_line(scene, code, 11)
            old_y = y
            y_decrement = Text(f"y = {old_y} - 1 = {old_y - 1}",
                             font="Monospace", font_size=10, color=YELLOW)
            y_decrement.next_to(cond_text, UP, buff=0.2)
            y_decrement.align_to(p_display, LEFT)
            scene.add(y_decrement)
            scene.wait(0.3)
            
            y -= 1
            
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.3)
            scene.remove(y_decrement)
            
            highlight_line(scene, code, 12)
            old_d = d2
            addition = Text(f"P = {old_d:.1f} + (2*rx_sq - 2*rx_sq*y + 2*ry_sq*x + 3*ry_sq + rx_sq)",
                          font="Monospace", font_size=9, color=YELLOW)
            addition.next_to(cond_text, UP, buff=0.2)
            addition.align_to(p_display, LEFT)
            scene.add(addition)
            scene.wait(0.4)
            
            d2 += (2 * rx_sq) - (2 * rx_sq * y) + (2 * ry_sq * x) + (3 * ry_sq) + rx_sq
            
            p_display.become(Text(f"P = {d2:.1f}", font="Monospace", font_size=48, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)
            scene.remove(addition)
        
        scene.remove(cond_text)
        scene.wait(0.2)
    
    scene.remove(code, title)

class GridEllipse(Scene):
    def construct(self):
        # Create grid
        grid = Grid(rows, cols)
        self.add(grid)
        self.wait(1)
        
        # Draw ellipse with center (35, 20), radii (12, 8) - centered in grid
        # Grid is 70x40, so center at (35, 20) with radii 12 and 8 fits perfectly
        xc, yc, rx, ry = 35, 20, 12, 8
        
        # Region 1
        x, y, rx_sq, ry_sq = region1_algorithm(self, grid, xc, yc, rx, ry)
        
        # Region 2 - continues from where region 1 left off
        region2_algorithm(self, grid, xc, yc, rx, ry, x, y, rx_sq, ry_sq)
        
        self.wait(3)
