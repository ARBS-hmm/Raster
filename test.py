from manim import *
from stack_module import AnimatedStack

class SimpleStackDemo(Scene):
    def construct(self):
        # Title
        title = Text("Animated Stack Demo", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create a stack
        stack = AnimatedStack(
            box_width=2.5,
            box_height=0.4,
            box_corner_radius=0.1,
            box_buff=0.1,
            font_size=14,
            max_visible=5,
            add_color=GREEN,
            base_color=BLUE,
            pop_color=RED
        )
        
        # Create the stack VGroup and position it
        stack_vgroup = stack.create_stack(
            center=ORIGIN,
            initial_count=0  # Start empty
        )
        
        # Add to scene
        self.add(stack_vgroup)
        
        # Set the scene for animations
        stack.set_scene(self)
        
        # Label the stack
        stack_label = Text("Stack", font_size=24, color=YELLOW)
        stack_label.next_to(stack_vgroup, UP, buff=0.5)
        self.play(Write(stack_label))
        self.wait(0.5)
        
        # Add elements one by one
        self.wait(1)
        self.add_element_animation(stack, "Apple")
        self.add_element_animation(stack, "Banana")
        self.add_element_animation(stack, "Cherry")
        self.add_element_animation(stack, "Date")
        self.add_element_animation(stack, "Elderberry")
        
        # Add one more - should push the bottom one out
        self.add_element_animation(stack, "Fig")
        
        # Pop two elements
        self.pop_element_animation(stack)
        self.pop_element_animation(stack)
        
        # Add another element
        self.add_element_animation(stack, "Grape")
        
        # Final wait
        self.wait(2)
    
    def add_element_animation(self, stack, text):
        """Helper to animate adding an element with a caption"""
        caption = Text(f"Adding: {text}", font_size=20, color=GREEN)
        caption.to_edge(DOWN)
        self.play(Write(caption), run_time=0.3)
        stack.add_element(text)
        self.play(FadeOut(caption), run_time=0.2)
        self.wait(0.3)
    
    def pop_element_animation(self, stack):
        """Helper to animate popping an element with a caption"""
        caption = Text("Popping top element", font_size=20, color=RED)
        caption.to_edge(DOWN)
        self.play(Write(caption), run_time=0.3)
        stack.pop_element()
        self.play(FadeOut(caption), run_time=0.2)
        self.wait(0.3)
