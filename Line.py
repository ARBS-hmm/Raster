from manim import *

rows,cols = 70,20

def set_pixel(grid, i, j, cols, color=BLUE, opacity=1):
    index = i * cols + j
    grid[index].set_fill(color=color, opacity=opacity)

def bresenham(grid,scene,x0: int, y0: int, x1: int, y1: int):
    dx = x1-x0
    dy = y1-y0
    x = x0
    y = y0
    P = 2*dy - dx
    while (x!=x1):
        set_pixel(grid,x,y,cols)
        scene.wait(1)
        if P <0 : 
            P+= 2*dy
        else: 
            y = y+1
            P+= (2*dy - 2*dx)
        x=x+1

class GridLine(Scene):
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
                )
        code = VGroup()
        PREFIX = "●"  # forces spaces to be non-leading

        lines = [
            "void bresenham(int x0, int y0, int x1, int y1) {"#1
            ,"   int dx = abs(x1 - x0);"#2
            ,"   int dy = abs(y1 - y0);"#3
            ,"   int x = x0;"#4
            ,"   int y = y0;"#5
            ,"   int P = 2*dy - dx;"#6
            ,"   while (x <= x1) {"#7
            ,"      putpixel(x, y);"#8
            ,"      if (P < 0) {"#9
            ,"         P += 2*dy;"#10
            ,"      } else {"#11
            ,"         y++;"#12
            ,"         P += 2*dy - 2*dx;"#13
            ,"      }"#14
            ,"      x++;"#15
            ,"   }"#16
            ,"}"#17
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

        self.wait(1)
        bresenham(grid,self,1,1,40,20)

        self.wait(10)

