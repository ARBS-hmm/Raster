from manim import *

def set_pixel(grid, i, j, cols, color=WHITE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

class GridCircle(Scene):
    def construct(self):
        rows, cols = 70, 30
        grid = VGroup()
        pixel = 0.2
        
        # Create pixel grid
        for i in range(rows):
            for j in range(cols):
                grid.add(
                    Square(pixel)
                    .set_stroke(color=WHITE, opacity=1, width=0.5)
                    .move_to([i * pixel, j * pixel, 0.0])
                )

        set_pixel(grid, 0, 0, cols)
        set_pixel(grid, 5, 10, cols)

        # ----- CODE BLOCK -----
        code = VGroup()

        PREFIX = "●"  # forces spaces to be non-leading
        lines = [
            "void circle(int xc, int yc, int r) {"#1
            ,"   int x = 0, y = r, d = 1 - r;"#2
            ,"   while (x <= y) {"#3
            ,"      putpixel(xc + x, yc + y);"#4
            ,"      putpixel(xc - x, yc + y);"#5
            ,"      putpixel(xc + x, yc - y);"#6
            ,"      putpixel(xc - x, yc - y);"#7
            ,"      putpixel(xc + y, yc + x);"#8
            ,"      putpixel(xc - y, yc + x);"#9
            ,"      putpixel(xc + y, yc - x);"#10
            ,"      putpixel(xc - y, yc - x);"#11
            ,"      if (d < 0) {"#12
            ,"         d += 2 * x + 3;"#13
            ,"      } else {"#14
            ,"         d += 2 * (x - y) + 5;"#15
            ,"         y--;"#16
            ,"      }"#17
            ,"      x++;"#18
            ,"   }"#19
            ,"}"#20
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

        self.add(grid)
        self.add(code)
        self.wait(10)
