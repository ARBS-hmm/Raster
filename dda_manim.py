from manim import *
from Grid import Grid

rows, cols = 70, 20

def set_pixel(grid, i, j, cols, color=BLUE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def dda(grid, scene, code_lines, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = float(x0)
    y = float(y0)

    # Create large steps display at bottom center
    steps_display = Text(f"steps = {steps}", font="Monospace", font_size=36, color=GREEN, weight=BOLD)
    steps_display.to_edge(DOWN, buff=0.8)
    scene.add(steps_display)

    # Create x, y, increments display above steps
    xy_display = Text(
        f"x = {x:.2f}    y = {y:.2f}    x_inc = {x_inc:.2f}    y_inc = {y_inc:.2f}",
        font="Monospace", font_size=14, color=WHITE
    )
    xy_display.next_to(steps_display, UP, buff=0.3)
    scene.add(xy_display)

    for i in range(steps + 1):
        # putpixel
        scene.highlight_code_line(code_lines, 8)
        set_pixel(grid, round(x), round(y), cols)

        # Update displays
        steps_display.become(
            Text(f"step = {i} / {steps}", font="Monospace", font_size=36, color=GREEN, weight=BOLD)
        )
        steps_display.to_edge(DOWN, buff=0.8)

        xy_display.become(
            Text(
                f"x = {x:.2f}    y = {y:.2f}    x_inc = {x_inc:.2f}    y_inc = {y_inc:.2f}",
                font="Monospace", font_size=14, color=WHITE
            )
        )
        xy_display.next_to(steps_display, UP, buff=0.3)
        scene.wait(0.5)

        # x = x + x_inc
        scene.highlight_code_line(code_lines, 9)
        x += x_inc
        scene.wait(0.4)

        # y = y + y_inc
        scene.highlight_code_line(code_lines, 10)
        y += y_inc
        scene.wait(0.4)

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
            "void dda(int x0, int y0, int x1, int y1) {",
            "   int dx = x1 - x0;",
            "   int dy = y1 - y0;",
            "   int steps = max(abs(dx), abs(dy));",
            "   float x_inc = dx / (float)steps;",
            "   float y_inc = dy / (float)steps;",
            "   float x = x0, y = y0;",
            "   for (int i = 0; i <= steps; i++) {",
            "      putpixel(round(x), round(y));",
            "      x += x_inc;",
            "      y += y_inc;",
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

        dda(grid, self, code, 1, 1, 40, 20)
        self.wait(5)
