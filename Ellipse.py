from manim import *
from Grid import Grid

rows, cols = 70, 40

def set_pixel(grid, i, j, cols, color=WHITE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def draw_ellipse_pixels(grid, scene, xc, yc, x, y):
    """
    Animate all 4 symmetric pixels one at a time.
    Each pixel flashes YELLOW with a floating coordinate label,
    then settles to WHITE.
    Labels are drawn in scene-space so they sit just above the pixel.
    """
    pixel_size = 0.2          # must match Grid() pixel size
    grid_origin = grid[0].get_center()   # position of pixel (0,0)

    # The four symmetric positions and their labels
    positions = [
        (xc + x, yc + y, f"({xc+x},{yc+y})"),
        (xc - x, yc + y, f"({xc-x},{yc+y})"),
        (xc + x, yc - y, f"({xc+x},{yc-y})"),
        (xc - x, yc - y, f"({xc-x},{yc-y})"),
    ]

    for pi, pj, label_str in positions:
        # --- flash pixel yellow ---
        set_pixel(grid, pi, pj, cols, color=YELLOW, opacity=1)

        # --- floating coordinate label ---
        # compute scene position of this pixel
        px_center = grid_origin + np.array([pi * pixel_size, pj * pixel_size, 0])
        coord_label = Text(label_str, font="Monospace", font_size=8, color=YELLOW)
        coord_label.move_to(px_center + UP * 0.25)
        scene.add(coord_label)

        scene.wait(0.25)

        # --- settle to white, remove label ---
        set_pixel(grid, pi, pj, cols, color=WHITE, opacity=1)
        scene.remove(coord_label)
        scene.wait(0.05)

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
    """Region 1 of midpoint ellipse algorithm (slope magnitude < 1, i.e. |dy/dx| < 1)"""
    region1_lines = [
        "void ellipse(int xc, int yc, int rx, int ry) {",   # 1
        "   int x=0, y=ry;",                                 # 2
        "   int rx2=rx*rx, ry2=ry*ry;",                      # 3
        "   float d1 = ry2 - rx2*ry + 0.25*rx2;",           # 4
        "   // Region 1: 2*ry2*x < 2*rx2*y",                # 5
        "   while (2*ry2*x < 2*rx2*y) {",                   # 6
        "      putpixel(xc±x, yc±y);",                      # 7
        "      if (d1 < 0) {",                               # 8
        "         d1 += 2*ry2*x + 3*ry2;",                  # 9
        "      } else {",                                    # 10
        "         y--;",                                     # 11
        "         d1 += 2*ry2*x - 2*rx2*y + 3*ry2 + 2*rx2;",# 12
        "      }",                                           # 13
        "      x++;",                                        # 14
        "   }",                                              # 15
        "}",                                                 # 16
    ]

    code, title = show_code(scene, region1_lines, "Region 1: |slope| < 1")

    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    d1 = ry2 - rx2 * ry + 0.25 * rx2

    # P value display
    p_display = Text(f"P = {d1:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD)
    p_display.to_edge(DOWN + LEFT, buff=0.8)
    scene.add(p_display)

    xy_display = Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE)
    xy_display.next_to(p_display, UP, buff=0.3)
    xy_display.align_to(p_display, LEFT)
    scene.add(xy_display)

    scene.wait(1)

    while (2 * ry2 * x) < (2 * rx2 * y):
        # Highlight while condition
        highlight_line(scene, code, 6)
        scene.wait(0.2)

        # Draw pixel — one at a time with flash + label
        highlight_line(scene, code, 7)
        draw_ellipse_pixels(grid, scene, xc, yc, x, y)

        # Update displays
        p_display.become(Text(f"P = {d1:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
        p_display.to_edge(DOWN + LEFT, buff=0.8)
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        xy_display.align_to(p_display, LEFT)

        # Check condition
        highlight_line(scene, code, 8)
        cond_text = Text(
            f"d1 {'<' if d1 < 0 else '>='} 0  ({d1:.2f})",
            font="Monospace", font_size=13, color=YELLOW
        )
        cond_text.next_to(xy_display, UP, buff=0.3)
        cond_text.align_to(p_display, LEFT)
        scene.add(cond_text)
        scene.wait(0.4)

        if d1 < 0:
            highlight_line(scene, code, 9)
            old_d = d1
            d1 += 2 * ry2 * x + 3 * ry2
            p_display.become(Text(f"P = {d1:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)
        else:
            highlight_line(scene, code, 11)
            y -= 1
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.2)

            highlight_line(scene, code, 12)
            d1 += 2 * ry2 * x - 2 * rx2 * y + 3 * ry2 + 2 * rx2
            p_display.become(Text(f"P = {d1:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)

        scene.remove(cond_text)
        highlight_line(scene, code, 14)
        x += 1

        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        xy_display.align_to(p_display, LEFT)
        scene.wait(0.3)

    scene.remove(code, title)
    scene.remove(p_display, xy_display)
    return x, y, rx2, ry2


def region2_algorithm(scene, grid, xc, yc, rx, ry, x, y, rx2, ry2):
    """Region 2 of midpoint ellipse algorithm (slope magnitude > 1, i.e. |dy/dx| > 1)"""
    region2_lines = [
        "   // Region 2: 2*ry2*x >= 2*rx2*y",               # 1
        "   float d2 = ry2*(x+0.5)*(x+0.5)",                 # 2
        "          + rx2*(y-1)*(y-1) - rx2*ry2;",            # 3
        "   while (y >= 0) {",                               # 4
        "      putpixel(xc±x, yc±y);",                      # 5
        "      if (d2 > 0) {",                               # 6
        "         y--;",                                     # 7
        "         d2 += -2*rx2*y + 3*rx2;",                  # 8
        "      } else {",                                    # 9
        "         x++;",                                     # 10
        "         y--;",                                     # 11
        "         d2 += 2*ry2*x - 2*rx2*y + 3*rx2 + 2*ry2;",# 12
        "      }",                                           # 13
        "   }",                                              # 14
    ]

    code, title = show_code(scene, region2_lines, "Region 2: |slope| > 1")

    # Calculate initial d2 for region 2
    d2 = ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2

    # P value display
    p_display = Text(f"P = {d2:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD)
    p_display.to_edge(DOWN + LEFT, buff=0.8)
    scene.add(p_display)

    xy_display = Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE)
    xy_display.next_to(p_display, UP, buff=0.3)
    xy_display.align_to(p_display, LEFT)
    scene.add(xy_display)

    scene.wait(1)

    while y >= 0:
        # Highlight while condition
        highlight_line(scene, code, 4)
        scene.wait(0.2)

        # Draw pixel — one at a time with flash + label
        highlight_line(scene, code, 5)
        draw_ellipse_pixels(grid, scene, xc, yc, x, y)

        # Update displays
        p_display.become(Text(f"P = {d2:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
        p_display.to_edge(DOWN + LEFT, buff=0.8)
        xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
        xy_display.next_to(p_display, UP, buff=0.3)
        xy_display.align_to(p_display, LEFT)

        # Check condition
        highlight_line(scene, code, 6)
        cond_text = Text(
            f"d2 {'>' if d2 > 0 else '<='} 0  ({d2:.2f})",
            font="Monospace", font_size=13, color=YELLOW
        )
        cond_text.next_to(xy_display, UP, buff=0.3)
        cond_text.align_to(p_display, LEFT)
        scene.add(cond_text)
        scene.wait(0.4)

        if d2 > 0:
            # Only y decrements
            highlight_line(scene, code, 7)
            y -= 1
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.2)

            highlight_line(scene, code, 8)
            d2 += -2 * rx2 * y + 3 * rx2
            p_display.become(Text(f"P = {d2:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)
        else:
            # Both x increments and y decrements
            highlight_line(scene, code, 10)
            x += 1
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.2)

            highlight_line(scene, code, 11)
            y -= 1
            xy_display.become(Text(f"x = {x}    y = {y}", font="Monospace", font_size=18, color=WHITE))
            xy_display.next_to(p_display, UP, buff=0.3)
            xy_display.align_to(p_display, LEFT)
            scene.wait(0.2)

            highlight_line(scene, code, 12)
            d2 += 2 * ry2 * x - 2 * rx2 * y + 3 * rx2 + 2 * ry2
            p_display.become(Text(f"P = {d2:.2f}", font="Monospace", font_size=36, color=GREEN, weight=BOLD))
            p_display.to_edge(DOWN + LEFT, buff=0.8)
            scene.wait(0.3)

        scene.remove(cond_text)
        scene.wait(0.1)

    scene.remove(code, title)
    scene.remove(p_display, xy_display)


class GridEllipse(Scene):
    def construct(self):
        # Create grid
        grid = Grid(rows, cols)
        self.add(grid)
        self.wait(1)

        # Draw ellipse with center (35, 20), rx=12, ry=8 — fits in 70x40 grid
        xc, yc, rx, ry = 35, 20, 12, 8

        # Region 1: starting from top of ellipse, moving right while |slope| < 1
        x, y, rx2, ry2 = region1_algorithm(self, grid, xc, yc, rx, ry)

        # Region 2: continuing from where region 1 stopped, moving down to rightmost point
        region2_algorithm(self, grid, xc, yc, rx, ry, x, y, rx2, ry2)

        self.wait(3)