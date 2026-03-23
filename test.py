from manim import *
from Stacklib import ManimStack

class StackDemo(Scene):
    def construct(self):
        # Create stack with same logic as your original code
        stack = ManimStack(
            box_width=2.5,
            box_height=0.4,
            box_corner_radius=0.1,
            box_buff=0.1,
            font_size=14,
            max_visible=5,
            stack_center=LEFT*5+DOWN*3
        )
        
        # Make the stack
        stack_vgroup = stack.make_stack(initial_count=5)  # Start empty
        self.add(stack_vgroup)
        stack.set_scene(self)
        
        # Add elements - EXACT same behavior as your code
        stack.add_element("New 1")
        stack.add_element("New 2")
        stack.add_element("New 3")
        stack.add_element("New 4")
        stack.add_element("New 5")
        stack.add_element("New 6")
        
        # Pop elements
        stack.pop_element()
        stack.pop_element()
        stack.pop_element()
        stack.pop_element()
        
        self.wait()
